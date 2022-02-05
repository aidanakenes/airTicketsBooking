from sanic import Sanic, response


async def booking(request):

    sample_response = {
         "id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"
        }

    return response.json({'test': sample_response})


async def booking_by_id(request, booking_id):
    return response.json({'test': booking_id})


async def booking_by_email_phone(request, email, phone):
    return response.json({'test': {'email': email, 'phone': phone}})
