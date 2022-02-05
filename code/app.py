from sanic import Sanic, response

from handlers import search

app = Sanic('air-tickets-booking')


def run():
    app.add_route(search.search, "/search")
    app.add_route(search.search_by_id, "/search/<search_id>")

    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
