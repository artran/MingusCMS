from datetime import datetime, timedelta

from django.contrib.auth.models import User

import unittest

from mingus.models import *

class LiveArticleTestCase(unittest.TestCase):
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