from django import template
from django.conf import settings

import logging

from mingus.cms.models import *

register = template.Library()


@register.simple_tag
def image_from_slug(slug, article, tag_end):
    'Return an img tag for the Image identified by the given slug for the given article'
    try:
        art_img = ArticleImage.objects.get(slug=slug, article=article)
        image = art_img.image
        image_url = image.get_absolute_url()
        image_alt_text = image.alt_text
        image_caption = image.caption
    except ArticleImage.DoesNotExist:
        logging.warning('No ArticleImage with the slug "%s" related to article "%s"' % (slug, article))
        image_url = 'NoImageFound'
        image_alt_text = 'NoImageFound'
        image_caption = 'NoImageFound'
    return u'<img href="%s" alt="%s" title="%s"%s' % (image_url, image_alt_text, image_caption, tag_end)
image_from_slug.is_safe = True


@register.simple_tag
def media_from_slug(slug, article):
    'Return a url for the Media identified by the given slug for the given article'
    try:
        art_media = ArticleMedia.objects.get(slug=slug, article=article)
        media_url = art_media.media.get_absolute_url()
    except ArticleMedia.DoesNotExist:
        logging.warning('No ArticleMedia with the slug "%s" related to article "%s"' % (slug, article))
        media_url = 'NoMediaFound'
    return media_url
media_from_slug.is_safe = True


@register.simple_tag
def text_from_slug(slug, article):
    'Return the text from the TextChunk identified by the given slug for the given article'
    try:
        article_tc = ArticleTextChunk.objects.get(slug=slug, article=article)
        text = article_tc.text_chunk.body
    except ArticleTextChunk.DoesNotExist:
        logging.warning('No ArticleTextChunk with the slug "%s" related to article "%s"' % (slug, article.slug))
        text = 'No TextChunks match'
    return text


@register.filter
def i18n_section_name(section, lang):
    return section.get_i18n_name(lang)


@register.filter
def i18n_article_title(article, lang):
    return article.get_i18n_title(lang)
