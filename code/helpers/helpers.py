import cache


async def convert_currency(request, data, currency):
    currency_cache = await cache.get_currency(request.app.ctx.redis)
    currency_price = 1.0

    for cur in currency_cache.get('rates').get('item'):
        currency_price = cur.get('description')

    for r in data.get('items'):
        r['price']['amount'], r['price']['currency'] = round(
            float(r.get('price').get('amount')) / float(currency_price), 2), currency

    return data
