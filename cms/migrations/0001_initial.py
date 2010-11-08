# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Language'
        db.create_table('cms_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('cms', ['Language'])

        # Adding model 'Section'
        db.create_table('cms_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('block_img', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('thumbnail_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('sort', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('sort_articles', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subsections', null=True, to=orm['cms.Section'])),
        ))
        db.send_create_signal('cms', ['Section'])

        # Adding M2M table for field allowed_groups on 'Section'
        db.create_table('cms_section_allowed_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm['cms.section'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False)),
        ))
        db.create_unique('cms_section_allowed_groups', ['section_id', 'group_id'])

        # Adding model 'TransSection'
        db.create_table('cms_transsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Section'])),
            ('trans_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cms', ['TransSection'])

        # Adding unique constraint on 'TransSection', fields ['lang', 'section']
        db.create_unique('cms_transsection', ['lang_id', 'section_id'])

        # Adding model 'Article'
        db.create_table('cms_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('head_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('style', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('live_from', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('live_to', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('feature', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('home_page', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('last_edited_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('last_edited_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edited_articles', to=orm['auth.User'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['cms.Section'])),
            ('sort', self.gf('django.db.models.fields.SmallIntegerField')(default=1000, null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['Article'])

        # Adding M2M table for field related on 'Article'
        db.create_table('cms_article_related', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_article', models.ForeignKey(orm['cms.article'], null=False)),
            ('to_article', models.ForeignKey(orm['cms.article'], null=False)),
        ))
        db.create_unique('cms_article_related', ['from_article_id', 'to_article_id'])

        # Adding model 'TransArticle'
        db.create_table('cms_transarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Article'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['TransArticle'])

        # Adding unique constraint on 'TransArticle', fields ['lang', 'article']
        db.create_unique('cms_transarticle', ['lang_id', 'article_id'])

        # Adding model 'ArticleImage'
        db.create_table('cms_articleimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['cms.Article'])),
        ))
        db.send_create_signal('cms', ['ArticleImage'])

        # Adding unique constraint on 'ArticleImage', fields ['slug', 'article']
        db.create_unique('cms_articleimage', ['slug', 'article_id'])

        # Adding model 'SectionImage'
        db.create_table('cms_sectionimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['cms.Section'])),
            ('thumbnail_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('cms', ['SectionImage'])

        # Adding unique constraint on 'SectionImage', fields ['slug', 'section']
        db.create_unique('cms_sectionimage', ['slug', 'section_id'])

    def backwards(self, orm):

        # Deleting model 'Language'
        db.delete_table('cms_language')

        # Deleting model 'Section'
        db.delete_table('cms_section')

        # Removing M2M table for field allowed_groups on 'Section'
        db.delete_table('cms_section_allowed_groups')

        # Deleting model 'TransSection'
        db.delete_table('cms_transsection')

        # Removing unique constraint on 'TransSection', fields ['lang', 'section']
        db.delete_unique('cms_transsection', ['lang_id', 'section_id'])

        # Deleting model 'Article'
        db.delete_table('cms_article')

        # Removing M2M table for field related on 'Article'
        db.delete_table('cms_article_related')

        # Deleting model 'TransArticle'
        db.delete_table('cms_transarticle')

        # Removing unique constraint on 'TransArticle', fields ['lang', 'article']
        db.delete_unique('cms_transarticle', ['lang_id', 'article_id'])

        # Deleting model 'ArticleImage'
        db.delete_table('cms_articleimage')

        # Removing unique constraint on 'ArticleImage', fields ['slug', 'article']
        db.delete_unique('cms_articleimage', ['slug', 'article_id'])

        # Deleting model 'SectionImage'
        db.delete_table('cms_sectionimage')

        # Removing unique constraint on 'SectionImage', fields ['slug', 'section']
        db.delete_unique('cms_sectionimage', ['slug', 'section_id'])

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
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feature': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'head_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'home_page': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_edited_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'last_edited_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edited_articles'", 'to': "orm['auth.User']"}),
            'live_from': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'live_to': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'blank': 'True', 'to': "orm['cms.Article']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1000', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.articleimage': {
            'Meta': {'unique_together': "(('slug', 'article'),)", 'object_name': 'ArticleImage'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['cms.Article']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.section': {
            'Meta': {'object_name': 'Section'},
            'allowed_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'block_img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsections'", 'null': 'True', 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {}),
            'sort_articles': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'thumbnail_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'cms.sectionimage': {
            'Meta': {'unique_together': "(('slug', 'section'),)", 'object_name': 'SectionImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['cms.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.transarticle': {
            'Meta': {'unique_together': "(('lang', 'article'),)", 'object_name': 'TransArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Article']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.transsection': {
            'Meta': {'unique_together': "(('lang', 'section'),)", 'object_name': 'TransSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Section']"}),
            'trans_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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
