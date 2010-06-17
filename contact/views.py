from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from forms import ContactForm
from models import *


def contact(request, form_id):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(form_id, request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            body = render_to_string('contact/contact.eml', {'post': request.POST})
            send_mail('Customer email from website', body, settings.DEFAULT_FROM_EMAIL,
                settings.CONTACT_RECIPIENTS, fail_silently=False)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm(form_id) # An unbound form

    return render_to_response('contact/contact.html', {
        'form': form,
    })


def list_forms(request):
    pass
