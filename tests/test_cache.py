import pytest

from code import cache


@pytest.mark.asyncio
async def test_save_get_search_results(redis_client, search_data, search_id):
    await cache.save_search_results(redis_client, search_data, search_id)
    search_results = await cache.get_search_results(redis_client, search_id)
    assert search_results.get('search_id')
    assert search_results.get('search_id') == search_id
    assert search_results.get('items')


@pytest.mark.asyncio
async def test_get_offer_results(redis_client, offer_id):
    offer_results = await cache.get_offer_results(redis_client, offer_id)

    assert list(offer_results.keys()) == [
        'id', 'flights', 'price', 'refundable', 'baggage', 'cabin', 'type', 'airline', 'passengers',
    ]
    assert offer_results.get('id') == offer_id


@pytest.mark.asyncio
async def test_get_offer_results_invalid(redis_client, invalid_offer_id):
    offer_results = await cache.get_offer_results(redis_client, invalid_offer_id)

    assert not offer_results


@pytest.mark.asyncio
async def test_get_currency(redis_client, currency_data):
    offer_results = await cache.get_currency(redis_client, currency_data)

    assert isinstance(offer_results, float)
