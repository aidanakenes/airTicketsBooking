from sanic import Sanic, response
import asyncpg
import aioredis
import httpx

import traceback
from datetime import datetime
import xmltodict

from handlers import search, offers, booking
import cache
import settings

app = Sanic('air-tickets-booking')


async def init_before(app, loop):
    app.ctx.db_pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL, loop=loop)
    app.ctx.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True, max_connections=50)


async def cleanup(app, loop):
    await app.ctx.redis.close()


async def server_error_handler(request, error: Exception):
    traceback.print_tb(error.__traceback__)
    status_code = error.status_code if hasattr(error, 'status_code') else 500
    return response.json({'error': str(error)}, status_code)


async def currency_update(app, loop):
    if await cache.get_currency(app.ctx.redis) is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get('https://www.nationalbank.kz/rss/get_rates.cfm',
                                     params={'fdate': datetime.today().strftime('%d.%m.%Y')}, timeout=30)
            data = xmltodict.parse(resp.text)
            await cache.save_currency(app.ctx.redis, data)


def run():
    app.register_listener(init_before, "before_server_start")
    app.register_listener(cleanup, "after_server_stop")
    app.register_listener(currency_update, "before_server_start")
    app.error_handler.add(Exception, server_error_handler)

    app.add_route(search.search, "/search", methods=["POST"])
    app.add_route(search.search_by_id, "/search/<search_id:str>", methods=["GET"])

    app.add_route(offers.offer_details, "/offers/<search_id:str>/<offer_id:str>", methods=["GET"])

    app.add_route(booking.create_booking, "/booking", methods=["POST"])
    app.add_route(booking.booking_details, "/booking/<booking_id:str>", methods=["GET"])
    app.add_route(booking.get_bookings, "/booking", methods=["GET"])

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
