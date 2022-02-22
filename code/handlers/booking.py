from sanic import Sanic, response
import jsonschema

import json
import httpx

import schemas
import db
import models


async def create_booking(request):
    jsonschema.validate(request.json, schema=schemas.BOOKING_SCHEMA)

    async with httpx.AsyncClient() as client:
        resp = await client.post('https://avia-api.k8s-test.aviata.team/offers/booking', json=request.json, timeout=30)
        booking_result = resp.json()

    if booking_result:
        booking_obj = models.Booking(booking_result)

        await db.create_booking(request.app.ctx.db_pool, booking_obj)

    return response.json(booking_result, dumps=json.dumps, default=str)


async def booking_details(request, booking_id):
    booking_details_result = await db.get_booking(request.app.ctx.db_pool, booking_id)

    return response.json(booking_details_result.__dict__(), dumps=json.dumps, default=str)


async def get_bookings(request):
    booking_list = await db.get_bookings(request.app.ctx.db_pool, request.args.get('email'), request.args.get('phone'), int(request.args.get('limit')))

    # %2B = + in url encoding
    return response.json([b.__dict__() for b in booking_list], dumps=json.dumps, default=str)
