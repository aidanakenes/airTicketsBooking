import json


async def cache_search(request, search_id):
    await request.app.redis.setex(f'internship:{search_id}', settings.REDIS_TTL, request.json)


async def get_search_cache(request, search_id):
    data = await request.app.ctx.redis.get(f'internship:{search_id}')
    return json.loads(data)


async def get_cache(request, offer_id):
    data = await request.app.ctx.redis.get(f'internship:{offer_id}')
    return json.loads(data)


async def save_currency(redis, currency_details):
    await redis.setex(f'currency', 86400, json.dumps(currency_details))


async def get_currency(redis):
    data = await redis.get(f'currency')
    if data is None:
        return

    return json.loads(data)


async def convert_currency(request, data):
    cached_currency = await request.app.ctx.redis.get(f'currency')
    currency_price = 1.0

    for cur in json.loads(cached_currency).get('rates').get('item'):
        currency_price = cur.get('description')

    for r in data.get('items'):
        r['price']['amount'], r['price']['currency'] = round(
            float(r.get('price').get('amount')) / float(currency_price), 2), request.json.get('currency')

    return data
