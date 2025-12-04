from typing import List
import aiohttp
from models.proxy_product import ProxyProduct, ProxyType


class ProxyProviderClient:
    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url
        self.api_key = api_key

    async def fetch_products(self) -> List[ProxyProduct]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with aiohttp.ClientSession(base_url=self.base_url, headers=headers) as session:
            # base_url=self.base_url — автоматически добавляет базовый URL ко всем запросам
            # (например, https://api.proxy.com + /products)
            async with session.get("/products") as resp:
                data = await resp.json()

        # Здесь адаптируем парсинг под реальный формат ответа поставщика
        products: List[ProxyProduct] = []
        for item in data["items"]:
            products.append(
                ProxyProduct(
                    id=int(item["id"]),
                    name=item["name"],
                    proxy_type=ProxyType(item["type"]),
                    country=item("country"),
                    period_days=int(item("period_days")),
                    quantity=int(item("quantity")),
                    price=float(item("price"))
                )
            )

        return products
