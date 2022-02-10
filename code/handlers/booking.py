from sanic import Sanic, response


async def create_booking(request):

    sample_response = {
         "id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"
        }

    return response.json({'test': sample_response})


async def booking_details(request, booking_id):
    return response.json({'test': booking_id})


async def get_bookings(request, email, phone):
    return response.json({'test': {'email': email, 'phone': phone}})
