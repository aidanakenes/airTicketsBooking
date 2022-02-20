from sanic import Sanic, response
import asyncpg

from handlers import search, offers, booking
import settings

app = Sanic('air-tickets-booking')


async def init_before(app, loop):
    app.ctx.db_pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL, loop=loop)


def run():
    app.register_listener(init_before, "before_server_start")

    app.add_route(search.search, "/search", methods=["POST"])
    app.add_route(search.search_by_id, "/search/<search_id:uuid>", methods=["GET"])

    app.add_route(offers.offer_details, "/offers/<offer_id:uuid>", methods=["GET"])

    app.add_route(booking.create_booking, "/booking", methods=["POST"])
    app.add_route(booking.booking_details, "/booking/<booking_id:str>", methods=["GET"])
    app.add_route(booking.get_bookings, "/booking", methods=["GET"])

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
