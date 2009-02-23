from django.conf.urls.defaults import *
from cms.models import *

#home_section = Section.objects.filter(live=True)[0]

#urlpatterns = patterns('',
#    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/articles/section/%i/' % home_section.id}),
#)

urlpatterns = patterns('cms.views',
    (r'^$', 'index'),
    (r'^section/(?P<slug>[-_0-9a-zA-Z]+)/$', 'section'),
    (r'^article/(?P<slug>[-_0-9a-zA-Z]+)/$', 'article'),
)
