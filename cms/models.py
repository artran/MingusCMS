from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from django.template import Template
from django.template.context import Context
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
    name = models.CharField(max_length=50, unique=True)
    live = models.BooleanField(default=False)
    slug = models.SlugField(help_text='Auto generated')
    sort = models.SmallIntegerField(help_text='Lower numbers sort earlier.')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subsections')
    allowed_groups = models.ManyToManyField(Group, blank=True)

    # Managers
    objects = models.Manager() # If this isn't first then non-live sections can't edited in the admin interface
    live_objects = LiveSectionManager()

    @staticmethod
    def get_sections_allowed_for_user(user=None):
        if user and user.is_authenticated():
            groups = user.groups.all().values('pk')
            return Section.live_objects.filter(Q(allowed_groups__in=groups)
                                               |
                                               Q(allowed_groups__isnull=True))
        else:
            return Section.live_objects.filter(allowed_groups__isnull=True)

    def get_i18n_name(self, language_code):
        try:
            name = TransSection.trans_sections.get(lang__code=language_code, section=self).name
        except TransSection.DoesNotExist:
            name = self.name
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
    section = models.ForeignKey(Section, related_name='trans_sections')
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        unique_together = ('lang', 'section')

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.name, self.section.name, self.lang.name)


class Article(models.Model):
    '''A model to hold the metadata and to pull all of the components together.'''
    ARTICLE_LIVE_TEST = "(live_from is null or live_from < %s) and (live_to is null or live_to > %s)"
    title = models.CharField(max_length=100)
    head_title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, help_text='For SEO purposes')
    keywords = models.TextField(blank=True, help_text='For SEO purposes')
    live_from = models.DateTimeField(blank=True, null=True, default=None, help_text='Blank means live immediately')
    live_to = models.DateTimeField(blank=True, null=True, default=None, help_text='Blank means live until forever')
    related = models.ManyToManyField('self', blank=True)
    slug = models.SlugField(unique=True, help_text='Auto generated')
    section = models.ForeignKey(Section, related_name='articles')
    sort = models.SmallIntegerField(default=1000, null=True, blank=True, help_text='Lower numbers sort earlier. Enable sorting in the section to use.')
    
    # Managers
    objects = models.Manager() # If this isn't first then non-live articles can't edited in the admin interface
    live_objects = LiveArticleManager()

    def get_i18n_title(self, language_code):
        try:
            title = TransArticle.trans_articles.get(lang__code=language_code, article=self).title
        except TransArticle.DoesNotExist:
            title = self.title
        return title

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

    @models.permalink
    def get_absolute_url(self):
        return('mingus.views.article', (self.slug,))


class TransArticle(models.Model):
    """The translation of an article's title and body text"""
    lang = models.ForeignKey(Language)
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = ('lang', 'article')

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.title, self.article.title, self.lang.name)


class AbstractMedia(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, help_text='Auto generated but can be overridden')
    caption = models.CharField(max_length=50, blank=True)

    # Set a slug if one wasn't provided.
    def save(self):
        # Set a slug if one isn't already set
        if not self.slug:
            self.slug = slugify(self.name)
        super(Image, self).save()

    def get_absolute_url(self):
        return self.image.url

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['id']


class Image(AbstractMedia):
    image = models.FileField(upload_to='cms_images')
    height = models.IntegerField()
    width = models.IntegerField()


class Media(AbstractMedia):
    media_file = models.FileField(upload_to='cms_media')
    mime_type = models.CharField(max_length=25)


class TextChunk(models.Model):
    body = models.TextField(blank=True)
    live = models.BooleanField(default=True)


class PageTemplate(models.Model):
    tmpl = models.FileField(upload_to='cms_templates')

    def render(self):
       ''' Turn the template content into HTML resolving variables and tags as it goes.'''
       template = Template(self.tmpl, name='Mingus article template for PageTemplate %s' % self.pk)
       c = Context({'settings': settings})
       return template.render(c)
