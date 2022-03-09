from sanic import response

import json
import asyncio
import uuid

from code import schemas
from code import jsonschema_
from code import cache
from code.helpers.helpers import convert_currency
from code.clients.aviata import Client
from code.helpers import errors


async def _collect_offers(request, search_id):
    for provider in ['Amadeus', 'Sabre']:
        request_data = json.loads(request.body)
        request_data['provider'] = provider
        provider_response = await Client(base_url='https://avia-api.k8s-test.aviata.team').search(**request_data)

        if request.json.get('currency') != 'KZT':
            provider_response = await convert_currency(request, provider_response.json(), request.json.get('currency'))

        provider_response['status'] = 'PENDING'
        await cache.save_search_results(request.app.ctx.redis, provider_response, search_id)

    await cache.update_search_status(request.app.ctx.redis, search_id, status='DONE')


async def search(request):
    await jsonschema_.validate(request.json, schemas.SEARCH_SCHEMA)
    if request.json.get('adults') < 1 and request.json.get('children') < 1 and request.json.get('infants') < 1:
        raise errors.PassengersNumberError()
    uid = str(uuid.uuid4())
    asyncio.create_task(_collect_offers(request, uid))

    return response.json({'search_id': uid})


async def search_by_id(request, search_id):
    search_results_by_id = await cache.get_search_results(request.app.ctx.redis, search_id)

    return response.json(search_results_by_id, dumps=json.dumps, default=str)
