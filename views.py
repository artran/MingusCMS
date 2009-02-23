from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext

from cms.models import *

def index(request):
    first_section = Section.live_objects.all()[0]
    return section(request, first_section.slug)

def section(request, slug):
    live_articles = Article.live_objects.filter(section__slug=slug)
    
    # Try to get a "home_page" article, if there are none use any article
    articles = live_articles.filter(home_page=True).order_by('?')
    if articles.count() > 0:
        the_article = articles[0]
    else:
        the_article = live_articles.order_by('?')[0]
    return article(request, the_article.slug)

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not article.is_live():
        raise Http404
    
    sections = Section.live_objects.filter(parent__isnull=True)
    live_articles = Article.live_objects.all()
    
    related = article.get_live_related()
    
    active = article.section
    while active.parent:
        active = active.parent
    return render_to_response('cms/article.html', {'sections': sections, 'article': article, 'active_section': active,
                        'related': related, 'in_this_section': live_articles, 'session': request.session, 'lang': request.LANGUAGE_CODE})
