from django.contrib import admin
from apps.bot_engine.models import *


@admin.register(ButtonsMedia)
class ButtonsMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media_id', 'button', 'created', 'updated')
    search_fields = ('id', 'media_id', 'button')


@admin.register(Buyproxy)
class ButtonsMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy', 'proxy', 'created', 'updated')
    search_fields = ('id', 'buy', 'proxy')


@admin.register(Buys)
class BuysAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_id', 'quantity', 'total_price', 'buy_datetime', 'is_refunded', 'created', 'updated')
    search_fields = ('id', 'buyer_id', )


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'name', 'proxy_type_id', 'country_id', 'period_days', 'quantity', 'price' ,'created', 'updated')
    search_fields = ('id', 'name', 'proxy_type_id', 'country_id', 'price')


@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user' ,'created', 'updated')
    search_fields = ('id', 'user')


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name', 'country_flag', 'created', 'updated')
    search_fields = ('id', 'country_name')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'processing_payment_id', 'message_id', 'is_paid', 'expire_datetime', 'created', 'updated')
    search_fields = ('id', 'user', 'processing_payment_id')


@admin.register(Periods)
class PeriodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'period_days', 'created', 'updated')
    search_fields = ('id', 'period_days')


@admin.register(Proxies)
class ProxiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_id', 'name', 'proxy_type_id', 'quantity', 'price', 'created', 'updated')
    search_fields = ('id', 'country_id', 'name', 'proxy_type_id')


@admin.register(ProxyTypes)
class ProxyTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'proxy_type', 'created', 'updated')
    search_fields = ('id', 'proxy_type')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_username', 'telegram_id', 'top_up_amount', 'consume_records', 'registered_at', 'can_receive_messages', 'created', 'updated')
    search_fields = ('id', 'telegram_username', 'telegram_id')




