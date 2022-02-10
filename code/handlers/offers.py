from sanic import Sanic, response


async def offer_details(request, offer_id):
    return response.json({'test': offer_id})
