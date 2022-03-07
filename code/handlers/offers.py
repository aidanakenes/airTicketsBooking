from sanic import Sanic, response

import json

from code import cache
from code.helpers import errors


async def offer_details(request, offer_id):

    offer_details_result = await cache.get_offer_results(request.app.ctx.redis, offer_id)

    if offer_details_result is None:
        raise errors.SearchNotFound()

    return response.json(offer_details_result, dumps=json.dumps, default=str)
