from django.conf.urls.defaults import *

urlpatterns = patterns('mingus.contact.views',
    (r'^(?P<form_id>\d+/$', 'contact'),
    (r'^thanks/(?P<form_id>\d+/$', 'thanks'),
)
