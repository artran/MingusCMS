from django.conf.urls.defaults import *
from mingus.models import *

urlpatterns = patterns('mingus.views',
    (r'^$', 'index'),
    (r'^section/(?P<slug>[-_0-9a-zA-Z]+)/$', 'section'),
    (r'^article/(?P<slug>[-_0-9a-zA-Z]+)/$', 'article'),
)
