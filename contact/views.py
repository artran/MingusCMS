from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string

from forms import ContactForm
from models import *


def contact(request, form_id):
    if request.method == 'POST':  # If the form has been submitted...
        form = ContactForm(form_id, request.POST)  # Will raise 404 if form id is invalid
        model = ContactFormModel.objects.get(pk=form_id)  # We know it's a valid id

        if form.is_valid():
            subject = render_to_string(model.subject_template, {'post': request.POST})
            body = render_to_string(model.body_template, {'post': request.POST})
            send_mail('Customer email from website', body, settings.DEFAULT_FROM_EMAIL,
                settings.CONTACT_RECIPIENTS, fail_silently=False)
            return redirect('thanks', form_id=form_id)
    else:
        form = ContactForm(form_id)

    return render_to_response(model.form_template, {
        'form': form,
    })


def thanks(request, form_id):
    contact_form = get_object_or_404(ContactFormModel, pk=form_id)
    return render_to_response(model.success_template, {})


def list_forms(request):
    pass
