from django.conf.urls.defaults import *

urlpatterns = patterns('mingus.contact.views',
    (r'^(?P<slug>\d+/$', 'contact'),
    (r'^thanks/(?P<slug>\d+/$', 'thanks'),
)
