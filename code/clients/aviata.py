import httpx
from helpers import errors
from code.clients import Client


class AviataClient(Client):

    def __init__(self):
        self._home = 'https://avia-api.k8s-test.aviata.team'
        self._endpoint = ''

    async def book(self):
        pass

    async def search(self):
        pass

