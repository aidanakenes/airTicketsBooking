import aioredis

from clients.nationalbank import NationalBankClient
import cache


async def update_currency():
    redis = await aioredis.from_url('redis://localhost', decode_responses=True, max_connections=50)
    currency_results = await NationalBankClient().get_currency_results()
    await cache.save_currency(redis, currency_results)
    await redis.close()

