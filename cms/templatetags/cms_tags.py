from django import template
from django.conf import settings

import logging

from mingus.cms.models import *

register = template.Library()


@register.simple_tag
def image_from_slug(slug, article):
    'Return an img tag for the Image identified by the given slug for the given article'
    try:
        art_img = ArticleImage.objects.get(slug=slug, article=article)
        image = art_img.image
        image_url = image.get_absolute_url()
        image_alt_text = image.alt_text
        image_caption = image.caption
    except ArticleImage.DoesNotExist:
        logging.warning('No images with the slug "%s" related to article "%s"' % (slug, article))
        image_url = 'NoImageFound'
        image_alt_text = 'NoImageFound'
        image_caption = 'NoImageFound'
    return u'<img href="%s" alt="%s" title="%s"/>' % (image_url, image_alt_text, image_caption)
image_from_slug.is_safe = True


@register.simple_tag
def media_from_slug(slug, article):
    'Return a url for the Media identified by the given slug for the given article'
    try:
        media = Media.get(slug=slug, article=article)
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
        chunk = TextChunk.get(slug=slug, article=article, live=True)
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
