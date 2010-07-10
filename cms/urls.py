from django.conf.urls.defaults import *
from django.contrib import admin

from models import *

admin.autodiscover()

urlpatterns = patterns('mingus.cms.views',
    (r'^$', 'index'),
    (r'^section/(?P<slug>[-_0-9a-zA-Z]+)/$', 'section'),
    (r'^article/(?P<slug>[-_0-9a-zA-Z]+)/$', 'article'),
)

urlpatterns += patterns('',
    # Admin:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
