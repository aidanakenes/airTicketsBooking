import pytest

invalid_book_data = {
    'offer_id': 'offer_id',
    'phone': 'phone',
    'email': 'email',
    'passengers': 'passengers',
}
book_data = {
    "offer_id": "d5a7a5b7-a4a3-49e7-9c69-b44d2cbe15cf",
    "phone": "+77777777777",
    "email": "user@example.com",
    "passengers": [
        {
            "gender": "M",
            "type": "ADT",
            "first_name": "Craig",
            "last_name": "Bensen",
            "date_of_birth": "1985-08-24",
            "citizenship": "US",
            "document": {
                "number": "N2343545634",
                "expires_at": "2025-08-24",
                "iin": "123456789123"
            }
        }
    ]
}

invalid_search_data = {
    "provider": 1,
    "cabin": "Economy",
    "origin": "ALA",
    "destination": "NQZ",
    "dep_at": "2022-02-09",
    "arr_at": "2022-02-15",
    "adults": 1,
    "children": 0,
    "infants": 0,
    'currency': 'USD',
}
search_data = {
    "provider": "Amadeus",
    "cabin": "Economy",
    "origin": "ALA",
    "destination": "NQZ",
    "dep_at": "2022-05-09",
    "arr_at": "2022-05-15",
    "adults": 1,
    "children": 0,
    "infants": 0,
    'currency': 'USD',
}
aviata_url = 'https://avia-api.k8s-test.aviata.team'


class TestAviataClient:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('url, expected_status, request_data', [
        (aviata_url, 404, book_data),
        (aviata_url, 422, invalid_book_data),
    ])
    async def test_book(self, url, expected_status, request_data):
        from code.clients.aviata import Client

        response = await Client(base_url=url).book(**request_data)
        assert response.status_code == expected_status

    @pytest.mark.parametrize('url, expected_status, request_data', [
        (aviata_url, 200, search_data),
        (aviata_url, 422, invalid_search_data),
    ])
    async def test_search(self, url, expected_status, request_data):
        from code.clients.aviata import Client

        response = await Client(base_url=url).search(**request_data)
        assert response.status_code == expected_status


national_bank_url = 'https://www.nationalbank.kz'


class TestNationalBankClient:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('url, expected_status', [
        (national_bank_url, 200),
    ])
    async def test_currency_results(self, url, expected_status):
        from code.clients.nationalbank import Client

        currency_results = await Client(base_url=url).get_currency_results()
        assert currency_results
