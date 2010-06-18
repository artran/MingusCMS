# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting model 'ArticleImage'
        db.delete_table('cms_articleimage')

        # Deleting model 'SectionImage'
        db.delete_table('cms_sectionimage')

        # Adding model 'Media'
        db.create_table('cms_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('media_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('cms', ['Media'])

        # Adding model 'Image'
        db.create_table('cms_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cms', ['Image'])

        # Adding model 'PageTemplate'
        db.create_table('cms_pagetemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tmpl', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cms', ['PageTemplate'])

        # Adding model 'TextChunk'
        db.create_table('cms_textchunk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('cms', ['TextChunk'])

        # Deleting field 'Section.sort_articles'
        db.delete_column('cms_section', 'sort_articles')

        # Deleting field 'Section.thumbnail_img'
        db.delete_column('cms_section', 'thumbnail_img')

        # Deleting field 'Section.block_img'
        db.delete_column('cms_section', 'block_img')

        # Deleting field 'Article.body'
        db.delete_column('cms_article', 'body')

        # Deleting field 'Article.home_page'
        db.delete_column('cms_article', 'home_page')

        # Deleting field 'Article.created_at'
        db.delete_column('cms_article', 'created_at')

        # Deleting field 'Article.feature'
        db.delete_column('cms_article', 'feature')

        # Deleting field 'Article.created_by'
        db.delete_column('cms_article', 'created_by_id')

        # Deleting field 'Article.last_edited_by'
        db.delete_column('cms_article', 'last_edited_by_id')

        # Deleting field 'Article.style'
        db.delete_column('cms_article', 'style')

        # Deleting field 'Article.last_edited_at'
        db.delete_column('cms_article', 'last_edited_at')

        # Deleting field 'TransArticle.body'
        db.delete_column('cms_transarticle', 'body')

        # Deleting field 'TransSection.trans_name'
        db.delete_column('cms_transsection', 'trans_name')

        # Adding field 'TransSection.name'
        db.add_column('cms_transsection', 'name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50), keep_default=False)

    def backwards(self, orm):

        # Adding model 'ArticleImage'
        db.create_table('cms_articleimage', (
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['cms.Article'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('cms', ['ArticleImage'])

        # Adding model 'SectionImage'
        db.create_table('cms_sectionimage', (
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('thumbnail_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['cms.Section'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('cms', ['SectionImage'])

        # Deleting model 'Media'
        db.delete_table('cms_media')

        # Deleting model 'Image'
        db.delete_table('cms_image')

        # Deleting model 'PageTemplate'
        db.delete_table('cms_pagetemplate')

        # Deleting model 'TextChunk'
        db.delete_table('cms_textchunk')

        # Adding field 'Section.sort_articles'
        db.add_column('cms_section', 'sort_articles', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'Section.thumbnail_img'
        db.add_column('cms_section', 'thumbnail_img', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'Section.block_img'
        db.add_column('cms_section', 'block_img', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'Article.body'
        db.add_column('cms_article', 'body', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Article.home_page'
        db.add_column('cms_article', 'home_page', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'Article.created_at'
        db.add_column('cms_article', 'created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True), keep_default=False)

        # Adding field 'Article.feature'
        db.add_column('cms_article', 'feature', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'Article.created_by'
        db.add_column('cms_article', 'created_by', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

        # Adding field 'Article.last_edited_by'
        db.add_column('cms_article', 'last_edited_by', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='edited_articles', to=orm['auth.User']), keep_default=False)

        # Adding field 'Article.style'
        db.add_column('cms_article', 'style', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Article.last_edited_at'
        db.add_column('cms_article', 'last_edited_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 6, 18, 18, 33, 48, 537372), blank=True), keep_default=False)

        # Adding field 'TransArticle.body'
        db.add_column('cms_transarticle', 'body', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'TransSection.trans_name'
        db.add_column('cms_transsection', 'trans_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50, unique=True), keep_default=False)

        # Deleting field 'TransSection.name'
        db.delete_column('cms_transsection', 'name')


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
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'live_from': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'live_to': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'blank': 'True', 'to': "orm['cms.Article']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
