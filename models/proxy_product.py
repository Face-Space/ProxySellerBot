from enum import Enum
from dataclasses import dataclass


class ProxyType(str, Enum):
    HTTPS = "https"
    SOCKS5 = "socks5"


@dataclass
class ProxyProduct:
    id: int
    name: str
    proxy_type: ProxyType
    country: str
    period_days: int
    quantity: int
    price: float

