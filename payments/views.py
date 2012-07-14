# Create your views here.
# coding=utf-8 

from models import *
from forms import *
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django_bitcoin.currency import *
from django_bitcoin.BCAddressField import b58encode

import django_bitcoin.templatetags

import django_bitcoin.views

from electrumpos.settings import electrum_wallet_server


def home(request):
    if request.method == "POST":
        merchant_form = MerchantForm(request.POST)
        if merchant_form.is_valid():
            merchant = merchant_form.save()
            merchant.uuid = b58encode(os.urandom(16))
            merchant.save()
            return HttpResponseRedirect("/m/"+merchant.uuid)
    else:
        merchant_form = MerchantForm()    

    return render_to_response("home.html", {
        "dummy": "dummy variable",
        "merchant_form": merchant_form,
        }, context_instance=RequestContext(request))


def payment(request, uuid):
    try:
        merchant = Merchant.objects.get(uuid=uuid)
    except Merchant.DoesNotExist:
        messages.add_message(request, messages.ERROR, \
                        _("Invalid secret URL."))
        return HttpResponseRedirect("/")

    payment = None
    fresh_payment = False

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            while True:
                payment.bitcoin_address = electrum_wallet_server.getnewaddress(merchant.master_public_key)
                if bitcoin_address_received(payment.bitcoin_address, 0) == Decimal(0):
                    break
            if not payment.bitcoin_address:
                raise Exception("Couldn't fetch new address. Contact the site operators.")
            payment.merchant = merchant
            payment.btc_amount = currency2btc(payment.currency_amount, merchant.currency)
            payment.save()
            fresh_payment = True
    else:
        payment_form = PaymentForm()
    
    if not payment and merchant.payment_set.all().count()>0:
        payment = merchant.payment_set.all().order_by("-created_at")[0] 

    previous_payments = Payment.objects.filter(merchant=merchant, archived_at=None).order_by("-created_at")

    return render_to_response("payment.html", {
        "merchant": merchant,
        "payment_form": payment_form,
        "payment": payment,
        "fresh_payment": fresh_payment,
        "previous_payments": previous_payments,
        }, context_instance=RequestContext(request))


