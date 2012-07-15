# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms
from django.forms import HiddenInput, RadioSelect, ModelForm, Textarea, Select, ValidationError, TextInput, ChoiceField, CheckboxInput
from django.utils.translation import ugettext_lazy as _
from payments import models
from decimal import Decimal
from models import Merchant, Payment

from electrumpos.settings import electrum_wallet_server

import os

from django_bitcoin.BCAddressField import b58encode


class MerchantForm(forms.ModelForm):

    master_public_key = forms.CharField(min_length=50,
        widget=forms.TextInput(attrs={'class': 'span8', 'placeholder': 'Your master public key'}))
 
    class Meta:
        model = Merchant
        fields = ("business_name", "currency",)

    def clean(self):

        success = electrum_wallet_server.new_wallet(self.cleaned_data["master_public_key"])
        if not success:
            raise ValidationError(_("Invalid public key."))

        return self.cleaned_data


class PaymentForm(forms.ModelForm):

    currency_amount = forms.DecimalField(label="", widget=forms.TextInput(attrs={'class': 'input-small', 'placeholder': _("Amount")}), )
    
    class Meta:
        model = Payment
        fields = ("currency_amount",)

    def clean(self):

        return self.cleaned_data
