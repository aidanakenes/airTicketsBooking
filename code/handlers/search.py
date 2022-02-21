from sanic import Sanic, response
import jsonschema
import httpx

import json

import schemas
import cache


async def search(request):
    jsonschema.validate(request.json, schema=schemas.SEARCH_SCHEMA)

    async with httpx.AsyncClient() as client:
        resp = await client.post('https://avia-api.k8s-test.aviata.team/offers/search', json=request.json, timeout=30)
        search_results = {
            'search_id': resp.json().get('search_id')
        }

        data = await cache.convert_currency(request, resp.json())

    await cache.cache_search(request, data)

    return response.json(search_results)


async def search_by_id(request, search_id):
    search_results_by_id = await cache.get_search_cache(request, search_id)

    return response.json(search_results_by_id, dumps=json.dumps, default=str)
