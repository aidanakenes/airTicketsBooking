import httpx
from helpers import errors


class AviataClient:

    def __init__(self):
        self._home = 'https://avia-api.k8s-test.aviata.team'
        self._endpoint = ''

    async def get_booking_request(self, params, endpoint):
        if endpoint == 'booking':
            self._endpoint = '/offers/booking'
        elif endpoint == 'search':
            self._endpoint = '/offers/search'

        async with httpx.AsyncClient() as client:
            provider_response = await client.post(
                f'{self._home}{self._endpoint}',
                json=params,
                timeout=30,
            )

        if provider_response is None:
            raise errors.SearchNotFound()

        return provider_response
