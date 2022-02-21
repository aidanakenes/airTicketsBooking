from sanic import Sanic, response
import httpx

import json

import cache


async def offer_details(request, search_id, offer_id):

    offer_details_result = await cache.get_search_cache(request, search_id)

    for offer in offer_details_result.get('items'):
        if offer.get('id') == offer_id:
            return response.json(offer, dumps=json.dumps, default=str)
