from sanic import Sanic, response

from handlers import search, offers, booking

app = Sanic('air-tickets-booking')


def run():
    app.add_route(search.search, "/search")
    app.add_route(search.search_by_id, "/search/<search_id>")

    app.add_route(offers.offers_by_id, "/offers/<offer_id>")

    app.add_route(booking.booking, "/booking")
    app.add_route(booking.booking_by_id, "/booking/<booking_id>")
    app.add_route(booking.booking_by_email_phone, "/booking/<email>/<phone>")

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
