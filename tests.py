from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

import unittest

from mingus.models import *


class LiveArticleTestCase(TestCase):

    def _create_default_sections(self):
        'Create some sections for testing'
        sec_not_live = Section(name='test not live', live=False, slug='test-not-live', sort=10)
        sec_not_live.save()
        sec_live = Section(name='test live', live=True, slug='test-live', sort=20)
        sec_live.save()

    def _create_default_articles(self):
        'Create a mix of articles for tests. Requires _create_default_sections to be run first'
        sec_not_live = Section.objects.get(slug='test-not-live')
        sec_live = Section.objects.get(slug='test-live')

        now = datetime.now()
        ten_ago = now - timedelta(minutes=10)
        ten_future = now + timedelta(minutes=10)
        user = User(username='test', password='password')
        user.save()

        # Live article in not live section
        nl1 = Article(title='lanls', body='', slug='lanls',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        section=sec_not_live)
        nl1.save()

        # Not live article in not live section
        nl2 = Article(title='nlanls', body='', slug='nlanls',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        live_to=ten_ago, section=sec_not_live)
        nl2.save()

        # Not live article in live section
        nl3 = Article(title='nlals', body='', slug='nlals',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        live_to=ten_ago, section=sec_live)
        nl3.save()

        # Live article in live section
        l1 = Article(title='lals', body='', slug='lals',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        section=sec_live)
        l1.save()

        # Live article by date in live section
        l2 = Article(title='lals2', body='', slug='lals2',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        live_from=ten_ago, live_to=ten_future, section=sec_live)
        l2.save()

        # Not live yet article in live section
        nl4 = Article(title='nlyals', body='', slug='nlyals',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        live_from=ten_future, section=sec_live)
        nl4.save()
        return {'nl1': nl1, 'nl2': nl2, 'nl3': nl3, 'nl4': nl4, 'l1': l1, 'l2': l2}

    def tearDown(self):
        Section.objects.all().delete()
        Article.objects.all().delete()

    def testNoContent(self):
        'Check 404 for the index view if the database is empty'
        art_url = reverse('mingus.views.index')
        response = self.client.get(art_url)
        self.failUnless(response.status_code == 404, 'Got %s instead of 404 for empty index.' % response.status_code)

    def testNoSuchSection(self):
        "Check 404 for a section which isn't in the db"
        art_url = reverse('mingus.views.section', kwargs={'slug': 'doesnotexist'})
        response = self.client.get(art_url)
        self.failUnless(response.status_code == 404, 'Got %s instead of 404 for non-existant section.' % response.status_code)

    def testNoSuchArticle(self):
        "Check 404 for an article which isn't in the db"
        art_url = reverse('mingus.views.article', kwargs={'slug': 'doesnotexist'})
        response = self.client.get(art_url)
        self.failUnless(response.status_code == 404, 'Got %s for non-existant page.' % response.status_code)

    def testSectionLive(self):
        'Check live section is included in sections list'
        self._create_default_sections()
        sec_live = Section.objects.get(slug='test-live')
        self.failUnless(sec_live in Section.live_objects.all())

    def testSectionNotLive(self):
        'Check non-live section is not included in sections list'
        self._create_default_sections()
        sec_not_live = Section.objects.get(slug='test-not-live')
        self.failIf(sec_not_live in Section.live_objects.all())

    def testLiveArticlesManager(self):
        'Check all combinations of article and section liveness work as expected'
        self._create_default_sections()
        articles = self._create_default_articles()

        live_arts = Article.live_objects.all()
        self.failIf(articles['nl1'] in live_arts)
        self.failIf(articles['nl2'] in live_arts)
        self.failIf(articles['nl3'] in live_arts)
        self.failIf(articles['nl4'] in live_arts)
        self.failUnless(articles['l1'] in live_arts)
        self.failUnless(articles['l2'] in live_arts)

    def testLiveArticle(self):
        'Check live article returns 200'
        self._create_default_sections()
        articles = self._create_default_articles()

        art_url = reverse('mingus.views.article', kwargs={'slug': articles['l1'].slug})
        response = self.client.get(art_url)
        self.failUnless(response.status_code == 200, 'Got status %s for live page.' % response.status_code)

    def testNonLiveArticle(self):
        'Check non live article returns 404'
        self._create_default_sections()
        articles = self._create_default_articles()

        art_url = reverse('mingus.views.article', kwargs={'slug': articles['nl1'].slug})
        response = self.client.get(art_url)
        self.failUnless(response.status_code == 404, 'Got %s for non-live page.' % response.status_code)


class SecureArticleTestCase(TestCase):

    fixtures = ('test-secure.xml',)
    
    def setUp(self):
        pass

    def tearDown(self):
        Article.objects.all().delete()
        Section.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()

    def test_not_auth(self):
        'Get the sections; secure_sec should be missing'

        url = reverse('mingus.views.index')
        secure_sec = Section.objects.get(slug='section-secure')

        response = self.client.get(url, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.failIf((secure_sec in response.context['sections']),
                'Sections contained secure section for unauth user')

    def test_insecure(self):
        'Login as user in insecure group and get the sections; secure_sec should be missing'

        url = reverse('mingus.views.index')
        secure_sec = Section.objects.get(slug='section-secure')

        self.client.login(username='user-insecure', password='password')
        response = self.client.get(url, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.failIf((secure_sec in response.context['sections']),
                'Sections contained secure section for insecure user')

    def test_insecure_article(self):
        'Get an article from secure_sec; it should 404'

        art_url = reverse('mingus.views.article', kwargs={'slug': 'sec_art'})

        response = self.client.get(art_url)
        self.failUnlessEqual(response.status_code, 404, 'Secure article returned for insecure user')

    def test_secure_sec(self):
        'Login as user in secure group and get the sections; secure_sec should be present'

        url = reverse('mingus.views.index')
        secure_sec = Section.objects.get(slug='section-secure')

        self.client.login(username='user-secure', password='password')
        response = self.client.get(url, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless((secure_sec in response.context['sections']),
                'Sections did not contain secure section for secure user')

    def test_secure_article(self):
        'Get an article from secure_sec; it should be present'

        art_url = reverse('mingus.views.article', kwargs={'slug': 'sec_art'})

        self.client.login(username='user-secure', password='password')
        response = self.client.get(art_url)
        self.failUnlessEqual(response.status_code, 200,
                'Secure article not returned for secure user')


class ArticleBannerImageTestCase(TestCase):

    fixtures = ('test-banner.xml',)
    
    def setUp(self):
        pass

    def tearDown(self):
        Article.objects.all().delete()
        Section.objects.all().delete()
        User.objects.all().delete()
        ArticleImage.objects.all().delete()

    def test_article_with_image(self):
        'Get an article which has a banner image. The image should be in the context'
        art_url = reverse('mingus.views.article', kwargs={'slug': 'banner_art'})

        response = self.client.get(art_url)
        self.failUnlessEqual(response.context['banner_image'].slug, 'banner_image',
                'No banner image returned')

    def test_article_without_banner_image(self):
        'Get an article which has no banner image. The context should contain None'
        art_url = reverse('mingus.views.article', kwargs={'slug': 'no_banner_art'})

        response = self.client.get(art_url)
        self.failUnlessEqual(response.context['banner_image'], None,
                'Banner image should be None')


class SortedArticlesTestCase(TestCase):

    fixtures = ('test-article-sorting.xml',)

    def test_sorted_articles(self):
        pass

class ContactEmailTest(TestCase):
    
    def test_send_email(self):
        'Send an email via the contact form and verify it reaches the mailbox'
        mail_url = reverse('mingus.views.contact')
        
        response = self.client.post(mail_url, {'first_name': 'Test',
                                               'last_name': 'Case',
                                               'email': 'test@artran.co.uk',
                                               'telephone': '0123456789',
                                               'comments': 'Test comments'})

        # Test that one message has been sent.
        self.assertEquals(len(mail.outbox), 1)
        self.failUnlessEqual(response.status_code, 200,
                'Status code was %s, should be 200' % response.status_code)
