from models.proxies import ProxyDTO


class MessageService:
    @staticmethod
    def create_message_with_bought_proxies(proxies: list[ProxyDTO]):
        message = "<b>"
        for count, proxy in enumerate(proxies, start=1):
            private_data = proxy.private_data
            message

