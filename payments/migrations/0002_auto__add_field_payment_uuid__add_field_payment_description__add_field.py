# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
import os
from payments.models import Payment


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Payment.uuid'
        db.add_column('payments_payment', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default='asd', unique=True, max_length=50),
                      keep_default=False)

        # Adding field 'Payment.description'
        db.add_column('payments_payment', 'description',
                      self.gf('django.db.models.fields.CharField')(default='Some payment', max_length=50),
                      keep_default=False)

        # Adding field 'Payment.currency'
        db.add_column('payments_payment', 'currency',
                      self.gf('django.db.models.fields.CharField')(default='USD', max_length=5),
                      keep_default=False)

        for p in Payment.objects.all():
            p.uuid = b58encode(os.urandom(16))


    def backwards(self, orm):
        # Deleting field 'Payment.uuid'
        db.delete_column('payments_payment', 'uuid')

        # Deleting field 'Payment.description'
        db.delete_column('payments_payment', 'description')

        # Deleting field 'Payment.currency'
        db.delete_column('payments_payment', 'currency')


    models = {
        'payments.merchant': {
            'Meta': {'object_name': 'Merchant'},
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master_public_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'payments.payment': {
            'Meta': {'object_name': 'Payment'},
            'archived_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'bitcoin_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'btc_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '5'}),
            'currency_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "'Some payment'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.Merchant']"}),
            'received_least': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '16', 'decimal_places': '8'}),
            'received_least_confirmed': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '16', 'decimal_places': '8'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'asd'", 'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['payments']