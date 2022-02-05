from sanic import Sanic, response


async def offers_by_id(request, offers_id):
    return response.json({'test': offers_id})
