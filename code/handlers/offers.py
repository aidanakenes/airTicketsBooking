from sanic import Sanic, response

import json

import cache


async def offer_details(request, offer_id):

    offer_details_result = await cache.get_offer(request.app.ctx.redis, offer_id)

    return response.json(offer_details_result, dumps=json.dumps, default=str)
