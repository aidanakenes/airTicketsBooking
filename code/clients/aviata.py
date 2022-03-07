from code.helpers import errors
from . import Client as BaseClient


class Client(BaseClient):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)

    async def book(self, offer_id, phone, email, passengers):
        data = {
            'offer_id': offer_id,
            'phone': phone,
            'email': email,
            'passengers': passengers,
        }

        provider_response = await self.post(url='/offers/booking', json=data)

        if provider_response is None:
            raise errors.BookNotFound()

        return provider_response

    async def search(self, provider, cabin, origin, destination, dep_at, arr_at, adults, children, infants, currency):
        data = {
            "provider": provider,
            "cabin": cabin,
            "origin": origin,
            "destination": destination,
            "dep_at": dep_at,
            "arr_at": arr_at,
            "adults": adults,
            "children": children,
            "infants": infants,
            "currency": currency
        }

        provider_response = await self.post(url='/offers/search', json=data)

        if provider_response is None:
            raise errors.SearchNotFound()

        return provider_response
