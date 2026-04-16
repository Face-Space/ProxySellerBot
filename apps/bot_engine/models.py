# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ButtonsMedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    media_id = models.CharField()
    button = models.TextField(unique=True)  # This field type is a guess.
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'buttons_media'


class Buyproxy(models.Model):
    id = models.BigAutoField(primary_key=True)
    buy = models.ForeignKey('Buys', models.DO_NOTHING)
    proxy = models.ForeignKey('Proxies', models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'buyProxy'


class Buys(models.Model):
    id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey('Users', models.DO_NOTHING)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    buy_datetime = models.DateTimeField()
    is_refunded = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'buys'


class CartItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey('Carts', models.DO_NOTHING)
    name = models.CharField()
    proxy_type_id = models.IntegerField()
    country_id = models.IntegerField()
    period_days = models.CharField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart_items'


class Carts(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carts'


class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    country_name = models.CharField(unique=True)
    country_flag = models.CharField(unique=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'countries'


class Payments(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    processing_payment_id = models.IntegerField()
    message_id = models.IntegerField()
    is_paid = models.BooleanField()
    expire_datetime = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payments'


class Periods(models.Model):
    id = models.BigAutoField(primary_key=True)
    period_days = models.CharField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'periods'


class Proxies(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING)
    name = models.CharField()
    proxy_type_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proxies'


class ProxyTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    proxy_type = models.CharField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proxy_types'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    telegram_username = models.CharField(unique=True)
    telegram_id = models.BigIntegerField(unique=True)
    top_up_amount = models.FloatField()
    consume_records = models.FloatField()
    registered_at = models.DateTimeField()
    can_receive_messages = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
