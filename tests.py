from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

import unittest

from mingus.models import *

class LiveArticleTestCase(TestCase):
    def setUp(self):
        sec_not_live = Section(name='test not live', live=False, slug='test-not-live', sort=10)
        sec_not_live.save()
        sec_live = Section(name='test live', live=True, slug='test-live', sort=20)
        sec_live.save()
    
    def tearDown(self):
        Section.objects.all().delete()
    
    def testSectionLive(self):
        sec_not_live = Section.objects.get(slug='test-not-live')
        sec_live = Section.objects.get(slug='test-live')
        
        self.failIf(sec_not_live in Section.live_objects.all())
        self.failUnless(sec_live in Section.live_objects.all())
    
    def testArticleLive(self):
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
                        live_from = ten_ago, live_to=ten_future, section=sec_live)
        l2.save()
        
        # Not live yet article in live section
        nl4 = Article(title='nlyals', body='', slug='nlyals',
                        created_by=user, created_at=now,
                        last_edited_by=user, last_edited_at=now,
                        live_from = ten_future, section=sec_live)
        nl4.save()
        
        # Now the tests
        live_arts = Article.live_objects.all()
        self.failIf(nl1 in live_arts)
        self.failIf(nl2 in live_arts)
        self.failIf(nl3 in live_arts)
        self.failIf(nl4 in live_arts)
        self.failUnless(l1 in live_arts)
        self.failUnless(l2 in live_arts)
        
        # Test for 404 on non-existant and non-live
        response = self.client.get('/articles/article/doesnotexist/')
        self.failUnless(response.status_code == 404, 'Got %s for non-existant page.' % response.status_code)
        
        response = self.client.get('/articles/article/%s/' % nl1.slug)
        self.failUnless(response.status_code == 404, 'Got %s for non-live page.' % response.status_code)
        
        # Check for 200 on existing page
        response = self.client.get('/articles/article/%s/' % l1.slug)
        self.failUnless(response.status_code == 404, 'Got status %s for live page.' % response.status_code)

class SecureArticleTestCase(TestCase):
    def setUp(self):
        group = Group(name='group-secure')
        group.save()

        insec_user = User.objects.create_user('user-insecure', 'insecure@artran.co.uk', 'password')

        sec_user = User.objects.create_user('user-secure', 'secure@artran.co.uk', 'password')
        sec_user.groups.add(group)
        sec_user.save()

        secure_sec = Section(name='test secure', live=True, slug='section-secure', sort=20)
        secure_sec.save()
        secure_sec.allowed_groups.add(group)
        secure_sec.save()

        insecure_sec = Section(name='test insecure', live=True, slug='section-insecure', sort=10)
        insecure_sec.save()

        now = datetime.now()
        sec_art = Article(title='sec_art', body='', slug='sec_art',
                        created_by=sec_user, created_at=now,
                        last_edited_by=sec_user, last_edited_at=now,
                        section=secure_sec)
        sec_art.save()

        insec_art = Article(title='insec_art', body='', slug='insec_art',
                        created_by=sec_user, created_at=now,
                        last_edited_by=sec_user, last_edited_at=now,
                        section=insecure_sec)
        insec_art.save()

    def tearDown(self):
        Article.objects.all().delete()
        Section.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()

    def test_not_auth(self):
        'Get the sections; secure_sec should be missing'

        url = reverse('mingus.views.index')
        secure_sec = Section.objects.get(slug='section-secure')

        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failIf((secure_sec in response.context['sections']),
                'Sections contained secure section for unauth user')

    def test_insecure(self):
        'Login as user in insecure group and get the sections; secure_sec should be missing'

        url = reverse('mingus.views.index')
        secure_sec = Section.objects.get(slug='section-secure')

        self.client.login(username='user-insecure', password='password')
        response = self.client.get(url)
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
        response = self.client.get(url)
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

