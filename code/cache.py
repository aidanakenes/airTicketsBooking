import json

import settings


async def generate_search_key(search_id):
    return f'internship: {search_id}'


async def generate_currency_key():
    return f'currency'


async def save_search(redis, search_data, search_id):
    await redis.setex(
        generate_search_key(search_id),
        settings.REDIS_SEARCH_TTL,
        json.dumps(search_data),
    )


async def get_search(redis, search_id):
    data = await redis.get(generate_search_key(search_id))

    if data:
        return json.loads(data)


async def save_currency(redis, currency_details):
    await redis.setex(
        generate_currency_key(),
        settings.REDIS_CURRENCY_TTL,
        json.dumps(currency_details)
    )


async def get_currency(redis):
    data = await redis.get(generate_currency_key())

    if data:
        return json.loads(data)
