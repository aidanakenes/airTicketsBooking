from sanic import Sanic, response

import json

from code import schemas
from code import jsonschema_
from code import db
from code import models
from code.clients.aviata import Client


async def create_booking(request):
    await jsonschema_.validate(request.json, schemas.BOOKING_SCHEMA)

    booking_result = await Client(base_url='https://avia-api.k8s-test.aviata.team').book(**json.loads(request.body))
    booking_obj = models.Booking(booking_result.json())

    await db.create_booking(request.app.ctx.db_pool, booking_obj)

    return response.json(booking_result.json(), dumps=json.dumps, default=str)


async def booking_details(request, booking_id):
    booking_details_result = await db.get_booking(request.app.ctx.db_pool, booking_id)

    return response.json(booking_details_result.__dict__(), dumps=json.dumps, default=str)


async def get_bookings(request):
    # %2B = + in url encoding
    booking_list = await db.get_bookings(
        request.app.ctx.db_pool,
        request.args.get('email'),
        request.args.get('phone'),
    )
    if booking_list:
        booking_pagination = await _pagination(booking_list, int(request.args.get('page')), int(request.args.get('limit')))

        return response.json(booking_pagination, dumps=json.dumps, default=str)


async def _pagination(data, page, limit):
    booking_pagination = []
    total = len(data)

    if limit > total:
        limit = 1

    for pagination in range(0, total, limit):
        booking_pagination.append({
            'page': pagination,
            'items': [b.__dict__() for b in data[page: pagination + limit]],
            'limit': limit,
            'total': total
        })

    if page > len(booking_pagination):
        page = 0

    return booking_pagination[page]
