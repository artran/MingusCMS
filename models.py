from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from datetime import datetime

from cms.middleware import threadlocals

import random

class LiveSectionManager(models.Manager):
    """Return only sections that are live"""
    def get_query_set(self):
        return super(LiveSectionManager, self).get_query_set().filter(live=True)

class LiveArticleManager(models.Manager):
    """Return only articles that are live"""
    def get_query_set(self):
        now = datetime.now()
        return super(LiveArticleManager, self).get_query_set().extra(where=[Article.ARTICLE_LIVE_TEST], params=[now, now]).filter(section__live=True)

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, help_text='Use the ISO 639-1 2-letter language code (see wikipedia)')
    class Admin:
        pass
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.code)

class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)
    live = models.BooleanField(default=False)
    slug = models.SlugField(prepopulate_from=('name',), help_text='Auto generated')
    block_img = models.ImageField(upload_to='block-images', help_text='800 x 279 image')
    thumbnail_img = models.ImageField(upload_to='icons', help_text='85 x 85 circular images')
    sort = models.SmallIntegerField(help_text='Lower numbers sort earlier.')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subsections')
    
    # Managers
    objects = models.Manager() # If this isn't first then non-live sections can't edited in the admin interface
    live_objects = LiveSectionManager()

    def get_random_image_url(self):
        # If there are no alternate images or the random function picks 0 from an appropriately sized range
        if self.images.count() == 0 or random.randrange(self.images.count()+1) == 0:
            return self.get_block_img_url()
        else:
            image = self.images.order_by('?')[0]
            return image.get_image_url()
    
    def get_i18n_name(self, language_code):
        name = self.name
        try:
            trans_sect = TransSection.objects.get(lang__code=language_code, section=self)
            name = trans_sect.trans_name
        except TransSection.DoesNotExist:
            pass
        return name
        
    def __unicode__(self):
        if self.live:
            return self.name
        else:
            return u'%s (not live)' % self.name
    class Meta:
        ordering = ['sort']
    class Admin:
        pass

class TransSection(models.Model):
    """The translation of a section's name"""
    lang = models.ForeignKey(Language)
    section = models.ForeignKey(Section)
    trans_name = models.CharField(max_length=50, unique=True)
    class Admin:
        list_display = ('trans_name', 'section', 'lang')
        list_filter = ['lang']
    class Meta:
        unique_together = ('lang', 'section')
    def __unicode__(self):
        return u'%s (%s, %s)' % (self.trans_name, self.section.name, self.lang.name)


class Article(models.Model):
    ARTICLE_LIVE_TEST = "(live_from is null or live_from < %s) and (live_to is null or live_to > %s)"
    title = models.CharField(max_length=100)
    body = models.TextField(help_text='For local images use {{ IMAGE[&lt;SLUG&gt;] }} or /media/cms_images/&lt;IMG-FILE&gt; for the url.')
    style = models.TextField('Extra styling', blank=True)
    live_from = models.DateTimeField(blank=True, null=True, default=None, help_text='Blank means live immediately')
    live_to = models.DateTimeField(blank=True, null=True, default=None, help_text='Blank means live until forever')
    home_page = models.BooleanField(default=False, help_text='Goes on the home page for a section')
    created_at = models.DateTimeField(blank=True, editable=False)
    created_by = models.ForeignKey(User, editable=False)
    last_edited_at = models.DateTimeField(blank=True, editable=False)
    last_edited_by = models.ForeignKey(User, related_name='edited_articles', editable=False)
    related = models.ManyToManyField('self', filter_interface=models.HORIZONTAL, blank=True)
    slug = models.SlugField(prepopulate_from=('title',), unique=True, help_text='Auto generated')
    section = models.ForeignKey(Section, related_name='articles')
    
    # Managers
    objects = models.Manager() # If this isn't first then non-live articles can't edited in the admin interface
    live_objects = LiveArticleManager()
    
    def get_i18n_title(self, language_code):
        title = self.title
        try:
            trans_article = TransArticle.objects.get(lang__code=language_code, article=self)
            title = trans_article.title
        except TransArticle.DoesNotExist:
            pass
        return title
    def get_i18n_body(self, language_code):
        body = self.body
        try:
            trans_article = TransArticle.objects.get(lang__code=language_code, article=self)
            body = trans_article.body
        except TransArticle.DoesNotExist:
            pass
        return body
    
    def get_live_related(self):
        'Return all of the related Articles which are live'
        now = datetime.now()
        return self.related.extra(where=[self.ARTICLE_LIVE_TEST], params=[now, now]).filter(section__live=True)
    
    def is_live(self):
        'Returns True if now is between live_from and live_to and the Section is live'
        now = datetime.now()
        return self.section.live == True and (self.live_from is None or self.live_from < now) and (self.live_to is None or self.live_to > now)
    
    # Set the creator and last_edited_by when appropriate
    def save(self):
        # If the object already existed, it will already have an id
        if not self.id:
            # This is a new object, set the creator 
            self.created_by = threadlocals.get_current_user()
            self.created_at = datetime.now()
        # All articles need the edited by and edited at fields setting
        self.last_edited_by = threadlocals.get_current_user()
        self.last_edited_at = datetime.now()
        super(Article, self).save()
        
    def __unicode__(self):
        if self.is_live():
            return self.title
        else:
            return u'%s (not live)' % self.title
    class Admin:
        save_on_top = True
        list_filter = ('section', 'created_by')
        search_fields = ('title',)
        list_display = ('title', 'live_from', 'live_to', 'is_live')

class TransArticle(models.Model):
    """The translation of an article's title and body text"""
    lang = models.ForeignKey(Language)
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=100)
    body = models.TextField(help_text='For local images use {{ IMAGE[&lt;SLUG&gt;] }} or /media/cms_images/&lt;IMG-FILE&gt; for the url.')
    class Admin:
        list_display = ('title', 'article', 'lang')
        list_filter = ['lang']
    class Meta:
        unique_together = ('lang', 'article')
    def __unicode__(self):
        return u'%s (%s, %s)' % (self.title, self.article.title, self.lang.name)

class Image(models.Model):
    name = models.CharField(max_length=30, core=True)
    slug = models.SlugField(prepopulate_from=('name',), blank=True, help_text='Auto generated but can be overridden')
    caption = models.CharField(max_length=50, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='cms_images', width_field='width', height_field='height', core=True)
    created_at = models.DateTimeField(blank=True, editable=False)
    created_by = models.ForeignKey(User, editable=False)
    
    # Set the creator fields when appropriate
    def save(self):
        # If the object already existed, it will already have an id
        if not self.id:
            # This is a new object, set the creator 
            self.created_by = threadlocals.get_current_user()
            self.created_at = datetime.now()
        
        # Set a slug if one isn't already set
        if not self.slug:
            self.slug = slugify(self.name)
        super(Image, self).save()
        
    def get_absolute_url(self):
        return self.get_image_url()
    def __str__(self):
        return self.name
    class Meta:
        abstract = True
        ordering = ['id']

class ArticleImage(Image):
    article = models.ForeignKey(Article, edit_inline=models.STACKED, related_name='images')
    class Admin:
        pass
    # I've comented this out after creation of the tables because it breaks the inline-editing in Articles.
    # As the uniqueness test is done in the db this shouldn't be an issue.
    #class Meta:
    #    unique_together = (('slug', 'article'),)

class SectionImage(Image):
    section = models.ForeignKey(Section, edit_inline=models.STACKED, related_name='images')
    thumbnail_img = models.ImageField(upload_to='icons', help_text='85 x 85 circular images')
    class Admin:
        pass
    # I've comented this out after creation of the tables because it breaks the inline-editing in Sections.
    # As the uniqueness test is done in the db this shouldn't be an issue.
    #class Meta:
    #    unique_together = (('slug', 'section'),)
    