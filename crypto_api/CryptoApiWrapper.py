import aiohttp


class CryptoApiWrapper:

    @staticmethod
    async def fetch_api_request(url: str, params: dict | None = None, method: str = "GET", data: str | None = None,
                                headers: dict | None = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, data=data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data

