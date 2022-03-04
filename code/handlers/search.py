from sanic import Sanic, response
import httpx

import json

import schemas
import jsonschema_
import cache
from helpers.helpers import convert_currency
from clients.aviata import Client
from helpers import errors


async def search(request):
    await jsonschema_.validate(request.json, schemas.SEARCH_SCHEMA)
    if request.json.get('adults') < 1 and request.json.get('children') < 1 and request.json.get('infants') < 1:
        raise errors.PassengersNumberError()

    provider_response = await Client(base_url='https://avia-api.k8s-test.aviata.team').search(**json.loads(request.body))
    search_results = {
        'search_id': provider_response.json().get('search_id')
    }

    if request.json.get('currency') is not 'KZT':
        provider_response = await convert_currency(request, provider_response.json(), request.json.get('currency'))

    await cache.save_search_results(request.app.ctx.redis, provider_response, search_results.get('search_id'))

    return response.json(search_results)


async def search_by_id(request, search_id):
    search_results_by_id = await cache.get_search_results(request.app.ctx.redis, search_id)

    return response.json(search_results_by_id, dumps=json.dumps, default=str)
