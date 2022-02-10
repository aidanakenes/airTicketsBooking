from sanic import Sanic, response


async def search(request):

    sample_result = {
        "id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"
    }

    return response.json(sample_result)


async def search_by_id(request, search_id):
    return response.json({'test': search_id})
