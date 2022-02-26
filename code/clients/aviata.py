from helpers import errors
from clients import Client


class AviataClient(Client):

    def __init__(self):
        super(AviataClient, self).__init__()

        self._home = 'https://avia-api.k8s-test.aviata.team'
        self._book_endpoint = '/offers/booking'
        self._search_endpoint = '/offers/search'

    async def book(self, params):
        provider_response = await super()._request(
            'POST',
            params,
            f'{self._home}{self._book_endpoint}',
        )

        if provider_response is None:
            raise errors.BookNotFound()

        return provider_response

    async def search(self, params):
        provider_response = await super()._request(
            'POST',
            params,
            f'{self._home}{self._search_endpoint}',
        )

        if provider_response is None:
            raise errors.SearchNotFound()

        return provider_response
