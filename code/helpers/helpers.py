from code import cache


async def convert_currency(request, data, currency):
    currency_price = await cache.get_currency(request.app.ctx.redis, currency)

    for r in data.get('items'):
        r['price']['amount'], r['price']['currency'] = round(
            float(r.get('price').get('amount')) / float(currency_price), 2), currency

    return data
