from sanic import Sanic, response


async def search(request):

    search_results = {
        "id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"
    }

    return response.json(search_results)


async def search_by_id(request, search_id):
    return response.json({'test': search_id})
