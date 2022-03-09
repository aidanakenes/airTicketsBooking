import pytest


@pytest.mark.asyncio
async def test_search(app, request_search_data):
    request, response = await app.asgi_client.post('/search', json=request_search_data)

    assert request.method == 'POST'
    assert response.status == 200
    assert response.json.get('search_id')
