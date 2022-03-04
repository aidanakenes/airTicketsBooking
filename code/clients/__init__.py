import httpx
from httpx._exceptions import TimeoutException

from helpers.decorators import retry


class Client:

    def __init__(self, base_url, *args, **kwargs):
        self._timeout = 30
        self._home = base_url

    async def _request(self, method_type, url, *args, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.request(method_type, f'{self._home}{url}', **kwargs)

        return response

    async def post(self, url, json=None, data=None, **kwargs):
        return await self._request('POST', url, json=json, data=data, **kwargs)

    async def get(self, url, json=None, params=None, **kwargs):
        return await self._request('GET', url, json=json, params=params, **kwargs)
