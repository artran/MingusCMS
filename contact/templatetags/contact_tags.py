from django.template import Library, Template
from django.template.context import Context

from contact.forms import ContactForm
from contact.models import ContactFormModel


register = Library()


@register.simple_tag
def contact_form(form_id):
    try:
        model = ContactFormModel.objects.get(pk=form_id, live=True)
        form = ContactForm(form_id)
        template = Template(model.form_template, name='Contact form template for form %s' % form_id)
        c = Context({'form': form})
        return template.render(c)
    except (ContactFormModel.DoesNotExist):
        return '<strong>Contact form %s does not exist or is not live.</strong>'
