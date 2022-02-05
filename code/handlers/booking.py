from sanic import Sanic, response


async def booking(request):

    sample_response = {
      "offer_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "phone": "+77777777777",
      "email": "user@example.com",
      "passengers": [
        {
          "gender": "M",
          "type": "ADT",
          "first_name": "CRAIGE",
          "last_name": "BENSEN",
          "date_of_birth": "1987-01-24",
          "citizenship": "US",
          "document": {
            "number": "N234346356",
            "expires_at": "2025-01-24",
            "iin": "123456789123"
          }
        }
      ]
    }

    return response.json({'test': sample_response})


async def booking_by_id(request, booking_id):
    return response.json({'test': booking_id})


async def booking_by_email_phone(request, email, phone):
    return response.json({'test': {'email': email, 'phone': phone}})
