from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

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
    return redirect(the_article)


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
    if section.sort_articles:
        in_this_section = Article.live_objects.filter(section=article.section).order_by('sort')
    else:
        in_this_section = Article.live_objects.filter(section=article.section).order_by('-home_page', '-feature', 'title')
    featured = in_this_section.filter(feature=True)

    related = article.get_live_related()

    # Try to get a 'banner' picture. If there isn't one then the section's banner can be used
    try:
        banner_image = article.images.filter(slug__istartswith='banner_image').order_by('?')[0]
    except IndexError:
        banner_image = None

    active = article.section
    while active.parent:
        active = active.parent
    return render_to_response('mingus/article.html', {'sections': sections,
                                                      'article': article,
                                                      'active_section': active,
                                                      'related': related,
                                                      'in_this_section': in_this_section,
                                                      'featured': featured,
                                                      'banner_image': banner_image,
                                                      'session': request.session,
                                                      'lang': request.LANGUAGE_CODE})

def contact(request):
    if request.method == 'POST':
        body = render_to_string('mingus/contact.eml', {'post': request.POST})
        send_mail('Customer email from website', body, settings.DEFAULT_FROM_EMAIL,
            settings.CONTACT_RECIPIENTS, fail_silently=False)
        return render_to_response('mingus/contact-sent.html')
    else:
        raise Http404
