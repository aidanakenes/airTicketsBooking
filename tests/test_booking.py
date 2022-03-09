import pytest


@pytest.mark.asyncio
async def test_create_booking(app, booking_data):
    request, response = await app.asgi_client.post('/booking', json=booking_data)

    assert request.method == 'POST'
    assert response.status == 200


@pytest.mark.asyncio
async def test_booking_details(app, booking_id):
    request, response = await app.asgi_client.get(f'/booking/{booking_id}')

    assert request.method == 'GET'
    assert response.status == 200
    assert response.json.get('id') == booking_id
