from sanic import Sanic, response
import jsonschema
import httpx

import json

import schemas
import cache
from helpers.helpers import convert_currency
from helpers import errors


async def search(request):
    try:
        jsonschema.validate(request.json, schema=schemas.SEARCH_SCHEMA)
    except jsonschema.ValidationError as e:
        raise errors.InvalidParams()

    if request.json.get('adults') < 1 and request.json.get('children') < 1 and request.json.get('infants') < 1:
        raise errors.PassengersNumberError()

    provider_response = await _get_provider_search(request.json)
    search_results = {
        'search_id': provider_response.json().get('search_id')
    }
    data = await convert_currency(request, provider_response.json(), request.json.get('currency'))
    await cache.save_search(request.app.ctx.redis, data, search_results.get('search_id'))

    return response.json(search_results)


async def search_by_id(request, search_id):
    search_results_by_id = await cache.get_search(request.app.ctx.redis, search_id)

    return response.json(search_results_by_id, dumps=json.dumps, default=str)


async def _get_provider_search(params):
    async with httpx.AsyncClient() as client:
        provider_response = await client.post(
            'https://avia-api.k8s-test.aviata.team/offers/search',
            json=params,
            timeout=30,
        )

    if provider_response is None:
        raise errors.SearchNotFound()

    return provider_response
