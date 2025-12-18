from aiogram.fsm.state import StatesGroup, State


class ProxyCatalog(StatesGroup):
    country = State()
    proxy_type = State()
    period = State()
    get_prox = State()
    proxies_quantity = State()
    payment = State()

