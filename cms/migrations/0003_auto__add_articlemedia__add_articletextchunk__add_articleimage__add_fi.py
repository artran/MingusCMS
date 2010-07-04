# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'ArticleMedia'
        db.create_table('cms_articlemedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Article'])),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Media'])),
        ))
        db.send_create_signal('cms', ['ArticleMedia'])

        # Adding model 'ArticleTextChunk'
        db.create_table('cms_articletextchunk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Article'])),
            ('text_chunk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.TextChunk'])),
        ))
        db.send_create_signal('cms', ['ArticleTextChunk'])

        # Adding model 'ArticleImage'
        db.create_table('cms_articleimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Article'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Image'])),
        ))
        db.send_create_signal('cms', ['ArticleImage'])

        # Adding field 'Article.template'
        db.add_column('cms_article', 'template', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='articles', null=True, to=orm['cms.PageTemplate']), keep_default=False)

    def backwards(self, orm):

        # Deleting model 'ArticleMedia'
        db.delete_table('cms_articlemedia')

        # Deleting model 'ArticleTextChunk'
        db.delete_table('cms_articletextchunk')

        # Deleting model 'ArticleImage'
        db.delete_table('cms_articleimage')

        # Deleting field 'Article.template'
        db.delete_column('cms_article', 'template_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cms.article': {
            'Meta': {'object_name': 'Article'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'head_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'blank': 'True', 'through': "'ArticleImage'", 'to': "orm['cms.Image']"}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'live_from': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'live_to': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'blank': 'True', 'through': "'ArticleMedia'", 'to': "orm['cms.Media']"}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'blank': 'True', 'to': "orm['cms.Article']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1000', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'to': "orm['cms.PageTemplate']"}),
            'text_chunks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'blank': 'True', 'through': "'ArticleTextChunk'", 'to': "orm['cms.TextChunk']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.articleimage': {
            'Meta': {'unique_together': "(('slug', 'article'),)", 'object_name': 'ArticleImage'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Image']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cms.articlemedia': {
            'Meta': {'unique_together': "(('slug', 'media'),)", 'object_name': 'ArticleMedia'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Media']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cms.articletextchunk': {
            'Meta': {'unique_together': "(('slug', 'text_chunk'),)", 'object_name': 'ArticleTextChunk'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'text_chunk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.TextChunk']"})
        },
        'cms.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.media': {
            'Meta': {'object_name': 'Media'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'cms.pagetemplate': {
            'Meta': {'object_name': 'PageTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tmpl': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'cms.section': {
            'Meta': {'object_name': 'Section'},
            'allowed_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsections'", 'null': 'True', 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cms.textchunk': {
            'Meta': {'object_name': 'TextChunk'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'cms.transarticle': {
            'Meta': {'unique_together': "(('lang', 'article'),)", 'object_name': 'TransArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.transsection': {
            'Meta': {'unique_together': "(('lang', 'section'),)", 'object_name': 'TransSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trans_sections'", 'to': "orm['cms.Section']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cms']
