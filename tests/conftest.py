import asyncio
import os
import sys

import asyncpg
import aioredis
import pytest

from code import models

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir))
sys.path.insert(0, PROJECT_ROOT)

db_dsn = 'postgres://postgres:aknsm@localhost/postgres'
cache_dsn = 'redis://localhost'


@pytest.fixture
def app():
    from code.app import app
    return app


@pytest.fixture
async def pool_database() -> asyncpg.pool.Pool:
    async with asyncpg.create_pool(db_dsn) as pool:
        yield pool


@pytest.fixture
async def redis_client() -> aioredis.Redis:
    redis: aioredis.Redis = await aioredis.from_url(url=cache_dsn, encoding='utf-8')
    yield redis
    await redis.close()


@pytest.fixture
def booking_id():
    return '93a02876-1f45-452f-853e-e09e8d9b886d'


@pytest.fixture
def filters():
    return {
        'email': 'aknsm@gmail.com',
        'phone': '+77777777777'
    }


@pytest.fixture
def currency_data():
    return 'USD'


@pytest.fixture
def search_id():
    return '557d187d-6465-4850-b4ea-6121752614f8'


@pytest.fixture
def offer_id():
    return '3c0d66ca-47e2-4e4e-9c9f-21b774b64a7f'


@pytest.fixture
def invalid_offer_id():
    return 'invalid-offer-id'


@pytest.fixture
def request_search_data():
    return {
        "provider": "Amadeus",
        "cabin": "Economy",
        "origin": "ALA",
        "destination": "NQZ",
        "dep_at": "2022-05-10",
        "arr_at": "2022-05-11",
        "adults": 2,
        "children": 0,
        "infants": 0,
        "currency": "RUB"
    }


@pytest.fixture
def search_data():
    return {
        "search_id": search_id,
        "items": [
            {
                "id": "3c0d66ca-47e2-4e4e-9c9f-21b774b64a7f",
                "flights": [
                    {
                        "duration": 18000,
                        "segments": [
                            {
                                "operating_airline": "DV",
                                "flight_number": "828",
                                "equipment": "Airbus A320-100/200",
                                "cabin": "Economy",
                                "dep": {
                                    "at": "2022-02-09T03:05:00+06:00",
                                    "airport": {
                                        "code": "ALA",
                                        "name": "Алматы"
                                    },
                                    "terminal": "4"
                                },
                                "arr": {
                                    "at": "2022-02-09T05:55:00+06:00",
                                    "airport": {
                                        "code": "CIT",
                                        "name": "Шымкент"
                                    },
                                    "terminal": "1"
                                },
                                "baggage": "1PC"
                            },
                            {
                                "operating_airline": "DV",
                                "flight_number": "958",
                                "equipment": "Boeing 767-200",
                                "cabin": "Economy",
                                "dep": {
                                    "at": "2022-02-09T09:15:00+06:00",
                                    "airport": {
                                        "code": "CIT",
                                        "name": "Шымкент"
                                    },
                                    "terminal": "3"
                                },
                                "arr": {
                                    "at": "2022-02-09T11:25:00+06:00",
                                    "airport": {
                                        "code": "NQZ",
                                        "name": "Нур-Султан (Астана)"
                                    },
                                    "terminal": "4"
                                },
                                "baggage": "1PC"
                            }
                        ]
                    }
                ],
                "price": {
                    "amount": 87736,
                    "currency": "KZT"
                },
                "refundable": True,
                "baggage": "1PC",
                "cabin": "Economy",
                "type": "OW",
                "airline": {
                    "code": "DV",
                    "name": "SCAT",
                    "logo": {
                        "url": "http://localhost/img/5661-501f546c73c976a96cf0d18e600b4d7a.gif",
                        "width": 1416,
                        "height": 274
                    }
                },
                "passengers": {
                    "ADT": 1,
                    "CHD": 0,
                    "INF": 0
                }
            }
        ]
    }


@pytest.fixture
def booking_data():
    return {
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


@pytest.fixture
def booking_obj():
    return models.Booking({
        "id": "93a02876-1f45-452f-853e-e09e8d9b886d",
        "pnr": "L1N3CW",
        "expires_at": "2022-03-07T22:04:40.297220+06:00",
        "phone": "+77777777777",
        "email": "aknsm@gmail.com",
        "offer": {
            "id": "e3b86160-e40c-4657-905b-a69b11741367",
            "flights": [
                {
                    "duration": 6300,
                    "segments": [
                        {
                            "operating_airline": "KC",
                            "flight_number": "752",
                            "equipment": "Boeing 747-400 Combi",
                            "cabin": "Economy",
                            "dep": {
                                "at": "2022-03-10T03:25:00+06:00",
                                "airport": {
                                    "code": "ALA",
                                    "name": "Алматы"
                                },
                                "terminal": "1"
                            },
                            "arr": {
                                "at": "2022-03-10T03:35:00+06:00",
                                "airport": {
                                    "code": "BXJ",
                                    "name": "Боралдай"
                                },
                                "terminal": "2"
                            },
                            "baggage": "1PC"
                        },
                        {
                            "operating_airline": "KC",
                            "flight_number": "973",
                            "equipment": "Boeing 747-100",
                            "cabin": "Economy",
                            "dep": {
                                "at": "2022-03-10T06:35:00+06:00",
                                "airport": {
                                    "code": "BXJ",
                                    "name": "Боралдай"
                                },
                                "terminal": "4"
                            },
                            "arr": {
                                "at": "2022-03-10T08:10:00+06:00",
                                "airport": {
                                    "code": "NQZ",
                                    "name": "Нур-Султан (Астана)"
                                },
                                "terminal": "4"
                            },
                            "baggage": "1PC"
                        }
                    ]
                },
                {
                    "duration": 17400,
                    "segments": [
                        {
                            "operating_airline": "KC",
                            "flight_number": "696",
                            "equipment": "Airbus A321neo Sharklet",
                            "cabin": "Economy",
                            "dep": {
                                "at": "2022-03-11T03:50:00+06:00",
                                "airport": {
                                    "code": "NQZ",
                                    "name": "Нур-Султан (Астана)"
                                },
                                "terminal": "9"
                            },
                            "arr": {
                                "at": "2022-03-11T08:40:00+06:00",
                                "airport": {
                                    "code": "ALA",
                                    "name": "Алматы"
                                },
                                "terminal": "4"
                            },
                            "baggage": "1PC"
                        }
                    ]
                }
            ],
            "price": {
                "amount": 184602,
                "currency": "KZT"
            },
            "refundable": True,
            "baggage": "1PC",
            "cabin": "Economy",
            "airline": {
                "code": "KC",
                "name": "Air Astana",
                "logo": {
                    "url": "https://avia-api.k8s-test.aviata.team/img/3093-fe65813d49024ba21b9ac7e21781fad5.svg",
                    "width": None,
                    "height": None
                }
            },
            "passengers": {
                "ADT": 2,
                "CHD": 0,
                "INF": 0
            },
            "type": "RT"
        },
        "passengers": [
            {
                "gender": "F",
                "type": "ADT",
                "first_name": "AIDANA",
                "last_name": "KENGES",
                "date_of_birth": "1987-01-24",
                "citizenship": "US",
                "document": {
                    "number": "N234346356",
                    "expires_at": "2025-01-24",
                    "iin": "123456789123"
                }
            },
            {
                "gender": "F",
                "type": "ADT",
                "first_name": "ALMAT",
                "last_name": "KENGES",
                "date_of_birth": "1987-01-24",
                "citizenship": "US",
                "document": {
                    "number": "N234346356",
                    "expires_at": "2025-01-24",
                    "iin": "123456789123"
                }
            }
        ]
    })
