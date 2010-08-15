from django.template import Template, Context
from django.test import TestCase

import os
import PIL

from mingus.cms.models import *


class ImageTagTest(TestCase):

    def setUp(self):
        f = open(settings.MEDIA_ROOT + '/test_image.png', 'w')
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
            title='art title', slug='article_slug',
            section=section,
        )

        art_img = ArticleImage.objects.create(
            slug='ai-slug', article=article, image=image,
        )

    def tearDown(self):
        os.remove(settings.MEDIA_ROOT + '/test_image.png')

    def test_image_tag(self):
        'Make sure image_from_slug gets correct image and fails gracefully'

        article = Article.objects.get(slug='article_slug')
        t = Template('{% load cms_tags %}{% image_from_slug slug article %}')
        c = Context({'slug': 'slug-wont-match', 'article': article})
        self.assertNotEqual(t.render(c).find('NoImageFound'), -1)

        c = Context({'slug': 'ai-slug', 'article': article})
        self.assertNotEqual(t.render(c).find('test_image.png'), -1)
