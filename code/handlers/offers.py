from sanic import Sanic, response


async def offers_by_id(request, offer_id):
    return response.json({'test': offer_id})
