# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Merchant'
        db.create_table('payments_merchant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('master_public_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='USD', max_length=5)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('payments', ['Merchant'])

        # Adding model 'Payment'
        db.create_table('payments_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('archived_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('bitcoin_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('btc_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=8)),
            ('currency_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.Merchant'])),
            ('received_least', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=16, decimal_places=8)),
            ('received_least_confirmed', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=16, decimal_places=8)),
        ))
        db.send_create_signal('payments', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Merchant'
        db.delete_table('payments_merchant')

        # Deleting model 'Payment'
        db.delete_table('payments_payment')


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
            'currency_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.Merchant']"}),
            'received_least': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '16', 'decimal_places': '8'}),
            'received_least_confirmed': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '16', 'decimal_places': '8'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['payments']