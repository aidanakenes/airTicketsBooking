from helpers import errors
from clients import Client

from datetime import datetime

import xmltodict


class NationalBankClient(Client):

    def __init__(self):
        super(NationalBankClient, self).__init__()

        self._home = 'https://www.nationalbank.kz/rss/get_rates.cfm'

    async def get_currency_results(self):
        provider_response = await super()._request(
            'GET',
            {'fdate': datetime.today().strftime('%d.%m.%Y')},
            f'{self._home}',
        )

        if provider_response is None:
            raise errors.BookNotFound()

        return xmltodict.parse(provider_response.text)

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
