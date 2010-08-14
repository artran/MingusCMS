from django import template
from django.conf import settings

from mingus.cms.models import *

register = template.Library()


@register.simple_tag
def image_from_slug(slug, article):
    'Return an img tag for the Image identified by the given slug for the given article'
    try:
        image = Image.get(slug=slug)
        image_url = image.get_absolute_url()
    except AssertionError:
        logging.warning('Multiple images found with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        image_url = 'MultipleImagesExist'
    except Image.DoesNotExist:
        logging.warning('No images with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        image_url = 'NoImageFound'
    return u'<img href="%s" alt="%s" title="%s"/>' % (image_url, image.alt_text, image.caption)
image_from_slug.is_safe = True


@register.simple_tag
def media_from_slug(slug, article):
    'Return a url for the Media identified by the given slug for the given article'
    try:
        media = Media.get(slug=slug)
        media_url = media.get_absolute_url()
    except AssertionError:
        logging.warning('Multiple media found with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        media_url = 'MultipleMediaExist'
    except Media.DoesNotExist:
        logging.warning('No media with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        media_url = 'NoMediaFound'
    return media_url
media_from_slug.is_safe = True


@register.simple_tag
def text_from_slug(slug, article):
    'Return the text from the TextChunk identified by the given slug for the given article'
    try:
        chunk = TextChunk.get(slug=slug, live=True)
        text = chunk.body
    except AssertionError:
        logging.warning('Multiple TextChunk found with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        text = 'Multiple TextChunks match'
    except TextChunk.DoesNotExist:
        logging.warning('No TextChunk with the slug "%s" related to article with slug "%s"' % (slug, article.slug))
        text = 'No TextChunks match'
    return text


@register.filter
def i18n_section_name(section, lang):
    return section.get_i18n_name(lang)


@register.filter
def i18n_article_title(article, lang):
    return article.get_i18n_title(lang)
