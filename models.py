from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from datetime import datetime

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
    '''
    Map ISO 639-1 codes to a friendly name.
    
    >>> en = Language(name='English', code='en')
    >>> fr = Language(name='French', code='fr')
    >>> en.save()
    >>> fr.save()
    >>> en
    <Language: English (en)>
    >>> Language.objects.get(code='en')
    <Language: English (en)>
    >>> Language.objects.count()
    2
    '''
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, help_text='Use the ISO 639-1 2-letter language code (see wikipedia)')

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.code)

class Section(models.Model):
    try:
        block_img_help_text = settings.SECTION_BLOCK_IMG_HELP
        thumb_img_help_text = settings.SECTION_THUMB_IMG_HELP
    except AttributeError:
        block_img_help_text = 'Configure help text in settings.SECTION_BLOCK_IMG_HELP'
        thumb_img_help_text = 'Configure help text in settings.SECTION_THUMB_IMG_HELP'
    name = models.CharField(max_length=50, unique=True)
    live = models.BooleanField(default=False)
    slug = models.SlugField(help_text='Auto generated')
    block_img = models.FileField(upload_to='block-images', blank=True, help_text=block_img_help_text)
    thumbnail_img = models.ImageField(upload_to='icons', blank=True, help_text=thumb_img_help_text)
    sort = models.SmallIntegerField(help_text='Lower numbers sort earlier.')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subsections')
    
    # Managers
    objects = models.Manager() # If this isn't first then non-live sections can't edited in the admin interface
    live_objects = LiveSectionManager()

    def get_random_image_url(self):
        # If there are no alternate images or the random function picks 0 from an appropriately sized range
        if self.images.count() == 0 or random.randrange(self.images.count()+1) == 0:
            return self.block_img.url
        else:
            image = self.images.order_by('?')[0]
            return image.image.url
    
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

class TransSection(models.Model):
    """The translation of a section's name"""
    lang = models.ForeignKey(Language)
    section = models.ForeignKey(Section)
    trans_name = models.CharField(max_length=50, unique=True)
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
    feature = models.BooleanField('Featured article', default=False, help_text='Sorts higher than non-feature articles in "in_this_section" context variable. Also given in "featured" context variable')
    home_page = models.BooleanField(default=False, help_text='Goes on the home page for a section. Sorts ahead of featured articles in "in_this_section" context variable.')
    created_at = models.DateTimeField(blank=True, editable=False, default=datetime.now)
    # The next three will be filled automatically in the admin interface. Outside the admin you still need to populate them.
    created_by = models.ForeignKey(User, editable=False)
    last_edited_at = models.DateTimeField(blank=True, editable=False)
    last_edited_by = models.ForeignKey(User, related_name='edited_articles', editable=False)
    related = models.ManyToManyField('self', blank=True)
    slug = models.SlugField(unique=True, help_text='Auto generated')
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
        
    def __unicode__(self):
        if self.is_live():
            return self.title
        else:
            return u'%s (not live)' % self.title

class TransArticle(models.Model):
    """The translation of an article's title and body text"""
    lang = models.ForeignKey(Language)
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=100)
    body = models.TextField(help_text='For local images use {{ IMAGE[&lt;SLUG&gt;] }} or /media/cms_images/&lt;IMG-FILE&gt; for the url.')
    class Meta:
        unique_together = ('lang', 'article')
    def __unicode__(self):
        return u'%s (%s, %s)' % (self.title, self.article.title, self.lang.name)

class Image(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, help_text='Auto generated but can be overridden')
    caption = models.CharField(max_length=50, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='cms_images')
    created_at = models.DateTimeField(blank=True, editable=False, default=datetime.now)
    created_by = models.ForeignKey(User, editable=False) # This will be filled automatically in the admin interface.
    
    # Set a slug if one wasn't provided.
    def save(self):
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
    article = models.ForeignKey(Article, related_name='images')
    class Meta:
        unique_together = (('slug', 'article'),)
try:
    img_help_text = settings.ARTICLE_IMG_HELP
except AttributeError:
    img_help_text = 'Configure help text in settings.ARTICLE_IMG_HELP'
ArticleImage._meta.get_field('image').help_text = img_help_text

class SectionImage(Image):
    try:
        img_help_text = settings.SECTION_ALT_THUMB_IMG_HELP
    except AttributeError:
        img_help_text = 'Configure help text in settings.SECTION_ALT_THUMB_IMG_HELP'
    section = models.ForeignKey(Section, related_name='images')
    thumbnail_img = models.ImageField(upload_to='icons', blank=True, help_text=img_help_text)
    class Meta:
        unique_together = (('slug', 'section'),)
try:
    img_help_text = settings.SECTION_ALT_IMG_HELP
except AttributeError:
    img_help_text = 'Configure help text in settings.SECTION_ALT_IMG_HELP'
SectionImage._meta.get_field('image').help_text = img_help_text
