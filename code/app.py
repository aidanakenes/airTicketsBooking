from sanic import Sanic, response

app = Sanic('air-tickets-booking')


def run():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
