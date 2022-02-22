from sanic import Sanic, response
import jsonschema

import json
import httpx

import schemas
import db
import models
from helpers import errors


async def create_booking(request):
    try:
        jsonschema.validate(request.json, schema=schemas.BOOKING_SCHEMA)
    except Exception as e:
        raise errors.InvalidParams()

    booking_result = await _get_provider_booking(request.json)
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


async def _get_provider_booking(params):
    async with httpx.AsyncClient() as client:
        provider_response = await client.post(
            'https://avia-api.k8s-test.aviata.team/offers/booking',
            json=params,
            timeout=30,
        )

    if provider_response is None:
        raise errors.SearchNotFound()

    return provider_response
