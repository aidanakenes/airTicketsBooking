from code.helpers import errors
from . import Client as BaseClient

from datetime import datetime

import xmltodict


class Client(BaseClient):

    def __init__(self, base_url, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)

    async def get_currency_results(self):
        params = {
            'fdate': datetime.today().strftime('%d.%m.%Y'),
        }

        provider_response = await self.get(url='/rss/get_rates.cfm', params=params)

        if provider_response is None:
            raise errors.CannotGetCurrencyDataFromProvider()

        return xmltodict.parse(provider_response.text)
