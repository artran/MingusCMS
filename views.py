from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext

from mingus.models import *

def index(request):
    try:
        first_section = Section.get_sections_allowed_for_user(request.user)[0]
    except IndexError:
        raise Http404
    return section(request, first_section.slug)

def section(request, slug):
    try:
        section = Section.get_sections_allowed_for_user(request.user).get(slug=slug)
    except Section.DoesNotExist:
        raise Http404

    live_articles = Article.live_objects.filter(section__slug=slug)
    
    # Try to get a "home_page" article, if there are none use any article
    articles = live_articles.filter(home_page=True).order_by('?')
    if articles.count() > 0:
        the_article = articles[0]
    elif live_articles.count() > 0:
        the_article = live_articles.order_by('?')[0]
    else:
        raise Http404
    return article(request, the_article.slug)

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not article.is_live():
        raise Http404
    sections = Section.get_sections_allowed_for_user(request.user)
    try:
        section = sections.get(slug=article.section.slug)
    except Section.DoesNotExist:
        raise Http404
    
    sections = sections.filter(parent__isnull=True)
    live_articles = Article.live_objects.all()
    in_this_section = Article.live_objects.filter(section=article.section).order_by('-home_page', '-feature', 'title')
    featured = in_this_section.filter(feature=True)
    
    related = article.get_live_related()
    
    active = article.section
    while active.parent:
        active = active.parent
    return render_to_response('mingus/article.html', {'sections': sections,
                                                      'article': article,
                                                      'active_section': active,
                                                      'related': related,
                                                      'in_this_section': in_this_section,
                                                      'featured': featured,
                                                      'session': request.session,
                                                      'lang': request.LANGUAGE_CODE})
