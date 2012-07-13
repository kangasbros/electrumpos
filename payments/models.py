from django.db import models
from django_bitcoin.currency import *
from decimal import Decimal
import datetime

# Create your models here.


class Merchant(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    master_public_key = models.CharField(max_length=50, unique=True)
    wallet_id = models.IntegerField(unique=True)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='USD')
    uuid = models.CharField(max_length=50)


class Payments(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, default=None)

    bitcoin_address = models.CharField(max_length=50)
    btc_amount = models.DecimalField(max_digits=16, decimal_places=8)

    currency_amount = models.DecimalField(max_digits=16, decimal_places=2)
