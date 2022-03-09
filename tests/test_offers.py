import pytest


@pytest.mark.asyncio
async def test_offer_details(app, offer_id):
    request, response = await app.asgi_client.get(f'/offers/{offer_id}')

    assert request.method == 'GET'
    assert response.status == 200
    assert response.json.get('id') == offer_id
