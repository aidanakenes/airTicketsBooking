from sanic import Sanic, response

from handlers import search, offers, booking

app = Sanic('air-tickets-booking')


def run():
    app.add_route(search.search, "/search", methods=["POST"])
    app.add_route(search.search_by_id, "/search/<search_id:uuid>", methods=["GET"])

    app.add_route(offers.offer_details, "/offers/<offer_id:uuid>", methods=["GET"])

    app.add_route(booking.booking, "/booking", methods=["POST"])
    app.add_route(booking.booking_by_id, "/booking/<booking_id:uuid>", methods=["GET"])
    app.add_route(booking.booking_by_email_phone, "/booking/<email:string>/<phone:[+,0-9]{0,4}>", methods=["GET"])

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
