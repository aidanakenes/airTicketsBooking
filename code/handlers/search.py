from sanic import Sanic, response


async def search(request):

    sample_result = {
      "provider": "Amadeus",
      "cabin": "Economy",
      "origin": "ALA",
      "destination": "NQZ",
      "dep_at": "2022-02-09",
      "arr_at": "2022-02-15",
      "adults": 1,
      "children": 0,
      "infants": 0,
      "currency": "KZT"
    }

    return response.json(sample_result)
