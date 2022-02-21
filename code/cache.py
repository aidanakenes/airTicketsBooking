import json

import settings


async def cache_search(request, search_id):
    await request.app.redis.setex(f'internship:{search_id}', settings.REDIS_TTL, request.json)


async def get_cache(request, offer_id):
    data = await request.app.ctx.redis.get(f'internship:{offer_id}')
    return json.loads(data)
