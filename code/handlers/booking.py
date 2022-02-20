from sanic import Sanic, response
import jsonschema

import schemas


async def create_booking(request):

    jsonschema.validate(request.json, schema=schemas.BOOKING_SCHEMA)

    booking_result = {}

    return response.json(booking_result)


async def booking_details(request, booking_id):

    booking_details_result = {}

    return response.json(booking_details_result)


async def get_bookings(request):

    booking_list = {'bookings': []}

    return response.json(booking_list)
