from django.db import models
from django_bitcoin.currency import *
from decimal import Decimal
import datetime
import urllib

from electrumpos.settings import SITE_URL

# Create your models here.

BITCOIN_CONFIRMATIONS_REQUIRED = getattr(
    settings, 
    "BITCOIN_CONFIRMATIONS_REQUIRED", 
    1)


def bitcoin_address_received(bitcoin_address, confirmations=BITCOIN_CONFIRMATIONS_REQUIRED):
    url = "http://blockchain.info/q/addressbalance/" + bitcoin_address + "?confirmations=" + str(confirmations)
    f = urllib.urlopen(url, None)
    data = f.read()
    r = Decimal(data) * Decimal("0.00000001")
    return r


class Merchant(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    master_public_key = models.CharField(max_length=255, unique=True)
    business_name = models.CharField(null=True, max_length=50)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='USD')
    uuid = models.CharField(max_length=50)

    def url(self):
        return "/m/"+self.uuid

    def full_url(self):
        return SITE_URL+self.url()


class Payment(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, default=None)

    bitcoin_address = models.CharField(max_length=50)
    btc_amount = models.DecimalField(max_digits=16, decimal_places=8)

    currency_amount = models.DecimalField(max_digits=16, decimal_places=2)

    merchant = models.ForeignKey(Merchant)

    received_least = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal(0))
    received_least_confirmed = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal(0))

    def payment_url(self):
        qr = "bitcoin:"+self.bitcoin_address+("", "?amount="+str(self.btc_amount))[self.btc_amount>0]
        if self.merchant.business_name:
            qr += "&label="+urllib.quote(str(self.merchant.business_name)+" #"+str(self.id))
        print qr
        print urllib.quote(qr)
        return urllib.quote(qr)

    def exchange_rate(self):
        return Decimal(self.currency_amount / self.btc_amount).quantize(Decimal("0.01"))
    
    # Return raw Bitcoin address
    def __unicode__(self):
        return "bitcoin:"+self.bitcoin_address+"&amount="+str(self.btc_amount)
    
    def received(self):
        r = bitcoin_address_received(self.bitcoin_address, confirmations=0)
        if r > self.received_least:
            self.received_least = r
            self.save()
        return r

    def received_confirmed(self):
        r = bitcoin_address_received(self.bitcoin_address, confirmations=BITCOIN_CONFIRMATIONS_REQUIRED)
        if r > self.received_least:
            self.received_least = r
            self.save()
        return r

    def is_paid(self):
        if self.received_least >= self.btc_amount:
            return True
        if self.received() >= self.btc_amount:
            return True
        return False

    def is_confirmed(self):
        if self.received_least_confirmed >= self.btc_amount:
            return True
        if self.received_confirmed() >= self.btc_amount:
            return True
        return False

    def url(self):
        return "/m/"+self.merchant.uuid+"/"+str(self.id)




