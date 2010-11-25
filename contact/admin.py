from django.contrib import admin
from models import *


class ElementAdmin(admin.ModelAdmin):
    pass


class FormElementInline(admin.TabularInline):
    model = ContactFormElements
    extra = 2


class ContactFormModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = (FormElementInline,)

admin.site.register(Element, ElementAdmin)
admin.site.register(ContactFormModel, ContactFormModelAdmin)
