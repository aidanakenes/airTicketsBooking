from sanic import Sanic, response

import json
import httpx

import schemas
import jsonschema_
import db
import models
from helpers import errors
from aviata_client import AviataClient


async def create_booking(request):
    jsonschema_.validate(request, schemas.BOOKING_SCHEMA)

    booking_result = await AviataClient().get_booking_request(request.json, 'booking')
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

    booking_pagination = []
    total = len(booking_list)
    limit = int(request.args.get('limit'))
    if limit > total:
        limit = total

    for page in range(0, total, limit):
        booking_pagination.append({
            'page': page,
            'items': [b.__dict__() for b in booking_list[page: page + limit]],
            'limit': limit,
            'total': total
        })

    page = int(request.args.get('page'))
    if page > len(booking_pagination):
        page = 0

    return response.json(booking_pagination[page], dumps=json.dumps, default=str)
