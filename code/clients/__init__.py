import httpx
from httpx._exceptions import TimeoutException

from helpers.decorators import retry


class Client:

    def __init__(self):
        self._timeout = 30

    @retry(exc_to_check=TimeoutException, tries=3, delay=3)
    async def _request(self, method_type, params, url):
        data = None
        if method_type == 'POST':
            data = params
            params = None

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method_type,
                url=url,
                params=params,
                json=data,
                timeout=self._timeout,
            )

        return response
