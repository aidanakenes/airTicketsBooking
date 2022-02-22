import json

import settings


async def save_search(redis, search_data, search_id):
    await redis.setex(
        f'internship:{search_id}',
        settings.REDIS_SEARCH_TTL,
        json.dumps(search_data),
    )


async def get_search(redis, search_id):
    data = await redis.get(f'internship:{search_id}')

    if data:
        return json.loads(data)


async def save_currency(redis, currency_details):
    await redis.setex(
        f'currency',
        settings.REDIS_CURRENCY_TTL,
        json.dumps(currency_details)
    )


async def get_currency(redis):
    data = await redis.get(f'currency')

    if data:
        return json.loads(data)
