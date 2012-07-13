# Create your views here.
# coding=utf-8 

from models import *
from forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail


def home(request):
    if request.method == "POST":
        merchant_form = MerchantForm(request.POST)
    else:
        merchant_form = MerchantForm()    

    return render_to_response("home.html", {
        "dummy": "dummy variable",
        "merchant_form": merchant_form,
        }, context_instance=RequestContext(request))


def payment(request, uuid):

    return render_to_response("payment.html", {
        "dummy": "dummy variable"
        }, context_instance=RequestContext(request))


