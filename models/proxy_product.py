from enum import Enum
from dataclasses import dataclass


class ProxyType(str, Enum):
    HTTPS = "http/s"
    SOCKS5 = "socks5"
    IPv4 = "IPv4"


@dataclass
class ProxyProduct:
    id: int
    name: str
    proxy_type: ProxyType
    country: str
    period_days: int
    quantity: int
    price: float

