# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Element'
        db.create_table('contact_element', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('widget_class', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('attrs', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('contact', ['Element'])

        # Adding model 'ContactFormModel'
        db.create_table('contact_contactformmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('form_template', self.gf('django.db.models.fields.TextField')()),
            ('recipient_list', self.gf('django.db.models.fields.TextField')()),
            ('subject_template', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body_template', self.gf('django.db.models.fields.TextField')()),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('contact', ['ContactFormModel'])

        # Adding model 'ContactFormElements'
        db.create_table('contact_contactformelements', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('element', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Element'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.ContactFormModel'])),
            ('sort', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('contact', ['ContactFormElements'])


    def backwards(self, orm):
        
        # Deleting model 'Element'
        db.delete_table('contact_element')

        # Deleting model 'ContactFormModel'
        db.delete_table('contact_contactformmodel')

        # Deleting model 'ContactFormElements'
        db.delete_table('contact_contactformelements')


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
            'elements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'form'", 'through': "'ContactFormElements'", 'to': "orm['contact.Element']"}),
            'form_template': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'recipient_list': ('django.db.models.fields.TextField', [], {}),
            'subject_template': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
