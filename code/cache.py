import json

import settings


async def generate_search_key(search_id):
    return f'search: {search_id}'


async def generate_currency_key():
    return f'currency'


async def save_search(redis, search_data, search_id):
    search_key = await generate_search_key(search_id)

    await redis.setex(
        search_key,
        settings.SEARCH_RESULTS_REDIS_TTL,
        json.dumps(search_data),
    )


async def get_search(redis, search_id):
    search_key = await generate_search_key(search_id)

    data = await redis.get(search_key)

    if data:
        return json.loads(data)


async def get_offer(redis, offer_id):
    cur = b'0'
    while cur:
        cur, keys = await redis.scan(cur, match='search:*')
        for key in keys:
            search_cache = await redis.get(key)

            if search_cache:
                search_cache = json.loads(search_cache)

                for offer_cache in search_cache.get('items'):
                    if offer_cache.get('id') == offer_id:
                        return offer_cache


async def save_currency(redis, currency_details):
    currency_key = await generate_currency_key()

    await redis.setex(
        currency_key,
        settings.CURRENCY_RESULTS_REDIS_TTL,
        json.dumps(currency_details)
    )


async def get_currency(redis):
    currency_key = await generate_currency_key()

    data = await redis.get(currency_key)

    if data:
        return json.loads(data)
