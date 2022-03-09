import json

from code import settings


async def generate_search_key(search_id, offer_id):
    return f'search:{search_id}:{offer_id}'


async def generate_currency_key(currency_to, currency_from):
    return f'currency:{currency_to}:{currency_from}'


async def save_search_results(redis, search_data, search_id):
    await redis.setex(
        search_id,
        settings.SEARCH_RESULTS_REDIS_TTL,
        json.dumps({'status': search_data.get('status')}),
    )

    for s in search_data.get('items'):
        search_key = await generate_search_key(search_id, s.get('id'))

        await redis.setex(
            search_key,
            settings.SEARCH_RESULTS_REDIS_TTL,
            json.dumps(s),
        )


async def update_search_status(redis, search_id, status):
    await redis.setex(
        search_id,
        settings.SEARCH_RESULTS_REDIS_TTL,
        json.dumps({'status': status}),
    )


async def get_search_results(redis, search_id):
    search_key = await generate_search_key(search_id, '*')

    search_status = await redis.get(search_id)
    search_cache_result = {
        'search_id': search_id,
        'status': json.loads(search_status).get('status'),
        'count': 0,
        'items': [],
    }

    cur = b'0'
    while cur:
        cur, keys = await redis.scan(cur, match=search_key, count=60)
        for key in keys:
            search_cache = await redis.get(key)

            if search_cache:
                search_cache_result.get('items').append(json.loads(search_cache))

    search_cache_result['count'] = len(search_cache_result.get('items'))

    return search_cache_result


async def get_offer_results(redis, offer_id):
    search_offer_key = await generate_search_key('*', offer_id)

    cur = b'0'
    while cur:
        cur, keys = await redis.scan(cur, match=search_offer_key, count=40)
        for key in keys:
            offer_cache = await redis.get(key)

            if offer_cache:
                return json.loads(offer_cache)


async def save_currency(redis, currency_details):
    for c in currency_details.get('rates').get('item'):
        currency_key = await generate_currency_key(c.get('title'), 'KZT')

        await redis.setex(
            currency_key,
            settings.CURRENCY_RESULTS_REDIS_TTL,
            float(c.get('description')),
        )


async def get_currency(redis, currency):
    currency_key = await generate_currency_key(currency, 'KZT')

    data = await redis.get(currency_key)

    if data:
        return json.loads(data)
