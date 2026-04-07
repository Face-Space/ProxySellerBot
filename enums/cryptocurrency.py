from enum import Enum


class Cryptocurrency(str, Enum):
    BNB = "BNB"
    BTC = "BTC"
    LTC = "LTC"
    ETH = "ETH"
    SOL = "SOL"
    USDT_SOL = "USDT_SOL"
    USDC_SOL = "USDC_SOL"
    USDT_ERC20 = "USDT_ERC20"
    USDC_ERC20 = "USDC_ERC20"
    USDT_BEP20 = "USDT_BEP20"
    USDC_BEP20 = "USDC_BEP20"


    def get_coingecko_name(self) -> str:
        match self:
            case Cryptocurrency.BTC:
                return "bitcoin"
            case Cryptocurrency.LTC:
                return "litecoin"
            case Cryptocurrency.ETH:
                return "ethereum"
            case Cryptocurrency.BNB:
                return "binancecoin"
            case Cryptocurrency.SOL:
                return "solana"
            case Cryptocurrency.USDT_SOL | Cryptocurrency.USDT_ERC20 | Cryptocurrency.USDT_BEP20:
                return "tether"
            case Cryptocurrency.USDC_SOL | Cryptocurrency.USDC_ERC20 | Cryptocurrency.USDC_BEP20:
                return "usd-coin"


    @staticmethod
    def get_stablecoins() -> list['Cryptocurrency']:
        return [Cryptocurrency.USDT_SOL, Cryptocurrency.USDC_SOL,
                Cryptocurrency.USDT_BEP20, Cryptocurrency.USDC_BEP20,
                Cryptocurrency.USDT_ERC20, Cryptocurrency.USDC_ERC20]

    # def __str__(self):
    #     return self.name
    #
    # def get_localized(self):
    #     return f"{self.name.lower()}_top_up"