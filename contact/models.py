from django.db import models


class Element(models.Model):
    'A component of a contact form.'
    ELEMENT_CHOICES = (
        ('char', 'CharField'),
        ('email', 'EmailField'),
        ('bool', 'BooleanField'),
        ('date', 'DateField'),
        ('dec', 'DecimalField'),
        ('int', 'IntegerField'),
    )

    name = models.CharField(max_length=20, unique=True, help_text='Memorable name for the component')
    field = models.CharField(max_length=10, choices=ELEMENT_CHOICES)
    default = models.CharField(max_length=25, blank=True)
    widget_class = models.CharField(max_length=25, blank=True)
    attrs = models.CharField(max_length=255, blank=True, help_text='HTML attributes in dict format')

    def __unicode__(self):
        return self.name


class ContactFormModel(models.Model):
    'A collection of form elements that know where to post to.'

    name = models.CharField(max_length=20, unique=True, help_text='Memorable name for the form.')
    form_template = models.TextField(help_text='Template code to produce the form.')
    recipient_list = models.TextField(help_text='Comma separated list of recipients.')
    subject_template = models.CharField(max_length=100, help_text='Template code to produce the email subject line.')
    body_template = models.TextField(help_text='Template code to produce the email body.')
    elements = models.ManyToManyField(Element, related_name='form', through='ContactFormElements')
    live = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ContactFormElements(models.Model):
    'A join model that allows the elements of a form to be ordered.'

    label = models.CharField(max_length=100, help_text='Label for this element.')
    element = models.ForeignKey(Element)
    form = models.ForeignKey(ContactFormModel)
    sort = models.PositiveSmallIntegerField(help_text='Low numbers sort first.')
    required = models.BooleanField(default=True)
