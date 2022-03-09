import pytest

from code import schemas

search_data = {
    "provider": "Amadeus",
    "cabin": "Economy",
    "origin": "ALA",
    "destination": "NQZ",
    "dep_at": "2022-05-09",
    "arr_at": "2022-05-15",
    "adults": 2,
    "children": 0,
    "infants": 0,
    "currency": 'USD',
}

invalid_search_data = {
    "provider": 3,
    "cabin": "Economy",
    "origin": "ALA",
    "destination": "NQZ",
    "dep_at": "2022-05-09",
    "arr_at": "2022-05-15",
    "adults": 1,
    "children": 0,
    "infants": 0,
}

booking_data = {
    "offer_id": "d5a7a5b7-a4a3-49e7-9c69-b44d2cbe15cf",
    "phone": "+77777777777",
    "email": "user@example.com",
    "passengers": [
        {
            "gender": "M",
            "type": "ADT",
            "first_name": "Craig",
            "last_name": "Bensen",
            "date_of_birth": "1985-08-24",
            "citizenship": "US",
            "document": {
                "number": "N2343545634",
                "expires_at": "2025-08-24",
                "iin": "123456789123"
            }
        }
    ]
}


@pytest.mark.asyncio
@pytest.mark.parametrize('request_data, schema, valid', [
    (booking_data, schemas.BOOKING_SCHEMA, True),
    (search_data, schemas.SEARCH_SCHEMA, True),
    (invalid_search_data, schemas.SEARCH_SCHEMA, False),
])
async def test_currency_results(request_data, schema, valid):
    from code import jsonschema_
    from code.helpers import errors
    try:
        await jsonschema_.validate(request_data, schema)
        assert valid
    except errors.InvalidParams as e:
        assert not valid
