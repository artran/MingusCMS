from django.template import Template, Context
from django.test import TestCase

import os
import PIL

from mingus.cms.models import *


class ImageTagTest(TestCase):
    IMAGE_FILE = settings.MEDIA_ROOT + '/test_image.png'

    def setUp(self):
        f = open(self.IMAGE_FILE, 'w')
        i = PIL.Image.new('RGBA', (10, 10,))
        i.save(f)
        f.close()

        image = Image(
            image='test_image.png', alt_text='alt',
            name='image for test', slug='img_slug',
        )
        image.save()

        section = Section.objects.create(
            name='sect', slug='sect_slug', sort=10, live=True,
        )

        article = Article.objects.create(
            title='art title', slug='article_slug', section=section,
        )

        ArticleImage.objects.create(
            slug='ai-slug', article=article, image=image,
        )

    def tearDown(self):
        os.remove(self.IMAGE_FILE)

    def test_image_tag(self):
        'Make sure image_from_slug gets correct image and fails gracefully'

        article = Article.objects.get(slug='article_slug')
        t = Template('{% load cms_tags %}{% image_from_slug slug article %}')
        c = Context({'slug': 'slug-wont-match', 'article': article})
        self.assertNotEqual(t.render(c).find('NoImageFound'), -1)

        c = Context({'slug': 'ai-slug', 'article': article})
        self.assertNotEqual(t.render(c).find(self.IMAGE_FILE.split('/')[-1]), -1)


class MediaTagTest(TestCase):
    FILE_NAME = 'test_media.txt'

    def setUp(self):
        media = Media(
            media_file=self.FILE_NAME, mime_type='text/plain',
            name='media for test', slug='media_slug',
        )
        media.save()

        section = Section.objects.create(
            name='sect', slug='sect_slug', sort=10, live=True,
        )

        article = Article.objects.create(
            title='art title', slug='article_slug', section=section,
        )

        ArticleMedia.objects.create(
            slug='am-slug', article=article, media=media,
        )

    def tearDown(self):
        pass

    def test_media_tag(self):
        'Make sure media_from_slug gets correct media and fails gracefully'

        article = Article.objects.get(slug='article_slug')
        t = Template('{% load cms_tags %}{% media_from_slug slug article %}')
        c = Context({'slug': 'slug-wont-match', 'article': article})
        self.assertNotEqual(t.render(c).find('NoMediaFound'), -1)

        c = Context({'slug': 'am-slug', 'article': article})
        self.assertNotEqual(t.render(c).find(self.FILE_NAME), -1)


class TextTagTest(TestCase):
    BODY_TEXT = 'Body text for test TextChunk'

    def setUp(self):
        txt = TextChunk.objects.create(
            body=self.BODY_TEXT, live=True,
        )

        section = Section.objects.create(
            name='sect', slug='sect_slug', sort=10, live=True,
        )

        article = Article.objects.create(
            title='art title', slug='article_slug', section=section,
        )

        art_img = ArticleTextChunk.objects.create(
            slug='atc-slug', article=article, text_chunk=txt,
        )

    def tearDown(self):
        pass

    def test_image_tag(self):
        'Make sure text_from_slug gets correct text and fails gracefully'

        article = Article.objects.get(slug='article_slug')
        t = Template('{% load cms_tags %}{% text_from_slug slug article %}')
        c = Context({'slug': 'slug-wont-match', 'article': article})
        self.assertNotEqual(t.render(c).find('No TextChunks match'), -1)

        c = Context({'slug': 'atc-slug', 'article': article})
        self.assertNotEqual(t.render(c).find(self.BODY_TEXT), -1)
