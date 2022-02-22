from sanic import Sanic, response
import asyncpg
import aioredis
import httpx
from httpx._exceptions import TimeoutException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import traceback
from datetime import datetime
import xmltodict

from handlers import search, offers, booking
from helpers import decorators
import cache
import settings

app = Sanic('air-tickets-booking')
scheduler = AsyncIOScheduler()


async def init_before(app, loop):
    app.ctx.db_pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL, loop=loop)
    app.ctx.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True, max_connections=50)


async def cleanup(app, loop):
    await app.ctx.redis.close()


async def server_error_handler(request, error: Exception):
    traceback.print_tb(error.__traceback__)
    status_code = error.status_code if hasattr(error, 'status_code') else 500
    return response.json({'error': str(error.__dict__)}, status_code)


@decorators.retry(exc_to_check=TimeoutException, tries=2, delay=2)
async def currency_update(app):
    if await cache.get_currency(app.ctx.redis) is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'https://www.nationalbank.kz/rss/get_rates.cfm',
                params={'fdate': datetime.today().strftime('%d.%m.%Y')},
                timeout=30,
            )

            data = xmltodict.parse(resp.text)
            await cache.save_currency(app.ctx.redis, data)


def run():
    app.register_listener(init_before, "before_server_start")
    app.register_listener(cleanup, "after_server_stop")
    scheduler.add_job(
        currency_update,
        trigger='cron',
        args=(app,),
        minute=59,
        hour=23,
        max_instances=1,
        replace_existing=True,
    )

    scheduler.start()
    app.error_handler.add(Exception, server_error_handler)

    app.add_route(search.search, "/search", methods=["POST"])
    app.add_route(search.search_by_id, "/search/<search_id:str>", methods=["GET"])

    app.add_route(offers.offer_details, "/offers/<offer_id:str>", methods=["GET"])

    app.add_route(booking.create_booking, "/booking", methods=["POST"])
    app.add_route(booking.booking_details, "/booking/<booking_id:str>", methods=["GET"])
    app.add_route(booking.get_bookings, "/booking", methods=["GET"])

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
