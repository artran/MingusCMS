# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'ContactFormModel.slug'
        db.add_column('contact_contactformmodel', 'slug', self.gf('django.db.models.fields.SlugField')(default=datetime.datetime(2010, 11, 25, 21, 12, 2, 719320), unique=True, max_length=50, db_index=True), keep_default=False)

    def backwards(self, orm):

        # Deleting field 'ContactFormModel.slug'
        db.delete_column('contact_contactformmodel', 'slug')

    models = {
        'contact.contactformelements': {
            'Meta': {'object_name': 'ContactFormElements'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Element']"}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.ContactFormModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'contact.contactformmodel': {
            'Meta': {'object_name': 'ContactFormModel'},
            'body_template': ('django.db.models.fields.TextField', [], {}),
            'elements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'form'", 'symmetrical': 'False', 'through': "orm['contact.ContactFormElements']", 'to': "orm['contact.Element']"}),
            'form_template': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'recipient_list': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'subject_template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'success_template': ('django.db.models.fields.TextField', [], {})
        },
        'contact.element': {
            'Meta': {'object_name': 'Element'},
            'attrs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'widget_class': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']
