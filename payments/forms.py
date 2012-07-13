# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms
from django.forms import HiddenInput, RadioSelect, ModelForm, Textarea, Select, ValidationError, TextInput, ChoiceField, CheckboxInput
from django.utils.translation import ugettext_lazy as _
from payments import models
from decimal import Decimal
from models import Merchant

import os

from django_bitcoin.BCAddressField import b58encode

class MerchantForm(forms.ModelForm):
 
    class Meta:
        model = Merchant
        fields = ("master_public_key","currency")

    def save(self):
        merchant = super(MerchantForm, self).save(commit=False)
        if not merchant.id:
            merchant.uuid = b58encode(os.urandom(16))
        return merchant

