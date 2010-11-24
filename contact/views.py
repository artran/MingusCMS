from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string

from forms import ContactForm
from models import *


def contact(request, form_id):
    if request.method == 'POST':  # If the form has been submitted...
        form = ContactForm(slug, request.POST)  # Will raise 404 if form id is invalid
        model = ContactFormModel.objects.get(slug=slug)  # We know it's a valid id

        if form.is_valid():
            subject = render_to_string(model.subject_template, {'post': request.POST})
            body = render_to_string(model.body_template, {'post': request.POST})
            send_mail('Customer email from website', body, settings.DEFAULT_FROM_EMAIL,
                settings.CONTACT_RECIPIENTS, fail_silently=False)
            return redirect('thanks', slug=slug)
    else:
        form = ContactForm(slug)

    return render_to_response(model.form_template, {
        'form': form,
    })


def thanks(request, slug):
    contact_form = get_object_or_404(ContactFormModel, slug=slug)
    return render_to_response(model.success_template, {})


def list_forms(request):
    pass
