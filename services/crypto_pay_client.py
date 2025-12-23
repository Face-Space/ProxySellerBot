import httpx

class CryptoPayClient:
    def __init__(self, token: str):
        self.base_url = "https://pay.crypt.bot/api"
        self.token = token
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Crypto-Pay-API-Token": self.token},
            timeout=10.0,
        )

    async def create_invoice(self, amount: float, asset: str, payload: str):
        data = {
            "amount": amount,
            "asset": asset,          # "USDT", "TON", etc.
            "payload": payload,      # твой internal id заказа/юзера
        }
        resp = await self.client.post("/createInvoice", json=data)
        resp.raise_for_status()
        return resp.json()["result"]
