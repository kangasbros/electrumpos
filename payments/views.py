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
from decimal import Decimal

import django_bitcoin.templatetags

import django_bitcoin.views

from electrumpos.settings import electrum_wallet_server

BITCOIN_CONVERSION_PRECISION = getattr(
    settings, 
    "BITCOIN_CONVERSION_PRECISION", 
    Decimal("0.0001"))

def home(request):
    if request.method == "POST":
        merchant_form = MerchantForm(request.POST)
        if merchant_form.is_valid():
            try:
                merchant = Merchant.objects.get(master_public_key=merchant_form.cleaned_data["master_public_key"])
                merchant.currency = merchant_form.cleaned_data["currency"]
                merchant.business_name = merchant_form.cleaned_data["business_name"]
                merchant.save()
            except Merchant.DoesNotExist:
                merchant = merchant_form.save(commit=False)
                merchant.master_public_key = merchant_form.cleaned_data["master_public_key"]
                merchant.uuid = b58encode(os.urandom(16))
                merchant.save()
            return HttpResponseRedirect("/m/"+merchant.uuid)
        else:
            messages.add_message(request, messages.ERROR, \
                        _("Error in form."))
    else:
        merchant_form = MerchantForm()    

    return render_to_response("home.html", {
        "dummy": "dummy variable",
        "merchant_form": merchant_form,
        }, context_instance=RequestContext(request))


def mpk(request, mpk, currency):
    try:
        merchant = Merchant.objects.get(master_public_key=mpk)
        merchant.currency = currency
        merchant.save()
    except Merchant.DoesNotExist:
        merchant = Merchant.objects.create(uuid=b58encode(os.urandom(16)), 
            master_public_key=mpk, currency=currency)
        merchant.save()
    return HttpResponseRedirect("/m/"+merchant.uuid)
        

def payment(request, uuid, payment_id=None):
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
            payment.btc_amount = currency2btc(payment.currency_amount, merchant.currency).quantize(BITCOIN_CONVERSION_PRECISION)
            payment.save()
            fresh_payment = True
            return HttpResponseRedirect(payment.url())
        else:
            messages.add_message(request, messages.ERROR, \
                        _("Error in form."))
    else:
        payment_form = PaymentForm()
    
    if payment_id:
        try:
            payment = Payment.objects.get(id=payment_id, merchant=merchant)
        except Payment.DoesNotExist:
            pass

    previous_payments = Payment.objects.filter(merchant=merchant, archived_at=None).order_by("-created_at")

    return render_to_response("payment.html", {
        "merchant": merchant,
        "payment_form": payment_form,
        "payment": payment,
        "fresh_payment": fresh_payment,
        "previous_payments": previous_payments,
        }, context_instance=RequestContext(request))


