from django.template import Template, Context
from django.test import TestCase

from mingus.cms.models import *

class ImageTagTest(TestCase):
    #def setUp(self):
        #image = Image.objects.create(
            #image='test_image.jpg', alt_text='alt',
            #name='image for test', slug='img_slug'
        #)
        #art = Article.objects.create()
        #art_img = Article.objects.create()

    def test_image_tag_for_no_image(self):
        t = Template('{% load cms_tags %}{% image_from_slug "slug" article %}')
        c = Context({'article': None})
        assert (t.render(c).find('NoImageFound') > -1)

    #def test_image_tag(self):
        #t = Template('{% load cms_tags %}{% image_from_slug "slug" article %}')
        #c = Context({'article': None})
        #assert (t.render(c).find('NoImageFound') > -1)
