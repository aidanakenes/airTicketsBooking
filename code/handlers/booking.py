from sanic import Sanic, response
import jsonschema

import schemas


async def create_booking(request):

    booking_result = {
        {
            "id": "ecdea60d-4b85-4f8b-98d0-4da07bb02f99",
            "pnr": "HKBTXK",
            "expires_at": "2022-01-23T15:10:14.411858+06:00",
            "phone": "+77013748830",
            "email": "example@mail.com",
            "offer": {
                "id": "826cf3e2-ea2a-4ee3-928a-3ded2b025a39",
                "flights": [
                    {
                        "duration": 12600,
                        "segments": [
                            {
                                "operating_airline": "KC",
                                "flight_number": "918",
                                "equipment": "Airbus A320-200 Sharklet",
                                "cabin": "Economy",
                                "dep": {
                                    "at": "2022-02-09T03:00:00+06:00",
                                    "airport": {
                                        "code": "ALA",
                                        "name": "Алматы"
                                    },
                                    "terminal": "4"
                                },
                                "arr": {
                                    "at": "2022-02-09T02:25:00+05:00",
                                    "airport": {
                                        "code": "GUW",
                                        "name": "Атырау"
                                    },
                                    "terminal": "4"
                                },
                                "baggage": "1PC"
                            },
                            {
                                "operating_airline": "KC",
                                "flight_number": "617",
                                "equipment": "Airbus A319-100 Sharklets",
                                "cabin": "Economy",
                                "dep": {
                                    "at": "2022-02-09T06:15:00+05:00",
                                    "airport": {
                                        "code": "GUW",
                                        "name": "Атырау"
                                    },
                                    "terminal": "1"
                                },
                                "arr": {
                                    "at": "2022-02-09T10:20:00+06:00",
                                    "airport": {
                                        "code": "NQZ",
                                        "name": "Нур-Султан (Астана)"
                                    },
                                    "terminal": "7"
                                },
                                "baggage": "1PC"
                            }
                        ]
                    }
                ],
                "price": {
                    "amount": 79522,
                    "currency": "KZT"
                },
                "refundable": True,
                "baggage": "1PC",
                "cabin": "Economy",
                "airline": {
                    "code": "KC",
                    "name": "Air Astana",
                    "logo": {
                        "url": "http://localhost/img/3093-fe65813d49024ba21b9ac7e21781fad5.svg"
                    }
                },
                "passengers": {
                    "ADT": 1,
                    "CHD": 0,
                    "INF": 0
                },
                "type": "OW"
            },
            "passengers": [
                {
                    "gender": "M",
                    "type": "ADT",
                    "first_name": "CRAIG",
                    "last_name": "BENSEN",
                    "date_of_birth": "1987-02-22",
                    "citizenship": "KZ",
                    "document": {
                        "number": "1341234234",
                        "expires_at": "2025-02-22",
                        "iin": "123456789123"
                    }
                }
            ]
        }
    }

    return response.json(booking_result)


async def booking_details(request, booking_id):

    jsonschema.validate(request.json, schema=schemas.BOOKING_DETAILS_SCHEMA)

    booking_details_result = {
        "id": "ecdea60d-4b85-4f8b-98d0-4da07bb02f99",
        "pnr": "HKBTXK",
        "expires_at": "2022-01-23T15:10:14.411858+06:00",
        "phone": "+77013748830",
        "email": "example@mail.com",
        "offer": {...},
        "passengers": [
            {
                "gender": "M",
                "type": "ADT",
                "first_name": "CRAIG",
                "last_name": "BENSEN",
                "date_of_birth": "1987-02-22",
                "citizenship": "KZ",
                "document": {
                    "number": "1341234234",
                    "expires_at": "2025-02-22",
                    "iin": "123456789123"
                }
            }
        ]
    }

    return response.json(booking_details_result)


async def get_bookings(request, email, phone):

    print(email, phone)
    booking_list = {'bookings': []}

    return response.json(booking_list)
