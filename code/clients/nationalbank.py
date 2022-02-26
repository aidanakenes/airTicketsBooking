import httpx
from helpers import errors
from code.clients import Client


class NationalBankClient(Client):

    def __init__(self):
        self._home = 'https://www.nationalbank.kz/rss/get_rates.cfm'
        self._endpoint = ''

    async def book(self):
        pass

    async def search(self):
        pass


# @decorators.retry(exc_to_check=TimeoutException, tries=2, delay=2)
# async def currency_update(app):
#     if await cache.get_currency(app.ctx.redis) is None:
#         async with httpx.AsyncClient() as client:
#             resp = await client.get(
#                 'https://www.nationalbank.kz/rss/get_rates.cfm',
#                 params={'fdate': datetime.today().strftime('%d.%m.%Y')},
#                 timeout=30,
#             )
#
#             data = xmltodict.parse(resp.text)
#             await cache.save_currency(app.ctx.redis, data)
