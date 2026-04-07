from aiogram.fsm.state import StatesGroup, State


class ProxyCatalog(StatesGroup):
    country = State()
    proxy_type = State()
    period = State()
    get_prox = State()
    proxies_quantity = State()
    payment = State()


class UserStates(StatesGroup):
    top_up_amount = State()
    review_image = State()
    review_text = State()
    shipping_address = State()
    filter_items = State()
    filter_purchase_history = State()
    coupon = State()
