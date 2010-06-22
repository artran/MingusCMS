from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from models import *


def index(request):
    try:
        first_section = Section.get_sections_allowed_for_user(request.user)[0]
    except IndexError:
        raise Http404
    return section(request, first_section.slug)


def section(request, slug):
    try:
        section = Section.get_sections_allowed_for_user(request.user).get(slug=slug)
        live_articles = Article.live_objects.filter(section__slug=slug).order_by('?')[0]
    except (Section.DoesNotExist, IndexError):
        raise Http404

    return redirect(the_article)


def article(request, slug):
    try:
        article = Article.live_objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    sections = Section.get_sections_allowed_for_user(request.user)
    try:
        section = sections.get(slug=article.section.slug)
    except Section.DoesNotExist:
        raise Http404

    sections = sections.filter(parent__isnull=True)
    live_articles = Article.live_objects.all()
    in_this_section = Article.live_objects.filter(section=article.section).order_by('sort')
    related = article.get_live_related()

    active = article.section
    while active.parent:
        active = active.parent
    return render_to_response('mingus/article.html', {'sections': sections,
                                                      'article': article,
                                                      'active_section': active,
                                                      'related': related,
                                                      'session': request.session,
                                                      'lang': request.LANGUAGE_CODE},
                                                      context_instance=RequestContext(request))
