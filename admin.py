from django.contrib import admin
from mingus.models import *

from datetime import datetime

class ArticleImageInline(admin.StackedInline):
    model = ArticleImage
    def save_model(self, request, img, form, change):
        if not change:
            img.created_by = request.user
        img.save()

class SectionImageInline(admin.StackedInline):
    model = SectionImage
    def save_model(self, request, img, form, change):
        if not change:
            img.created_by = request.user
        img.save()

class SectionAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    inlines = (SectionImageInline,)

class TransSectionAdmin(admin.ModelAdmin):
    list_display = ('trans_name', 'section', 'lang')
    list_filter = ['lang']

class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ('section', 'created_by')
    search_fields = ('title',)
    list_display = ('title', 'section', 'live_from', 'live_to', 'is_live')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ArticleImageInline,)
    filter_horizontal = ('related',)
    def save_model(self, request, article, form, change):
        if not change:
            article.created_by = request.user
        article.last_edited_by = request.user
        article.last_edited_at = datetime.now()
        article.save()

class TransArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'lang')
    list_filter = ['lang']

class ArticleImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    def save_model(self, request, image, form, change):
        if not change:
            image.created_by = request.user
        image.save()

class SectionImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    def save_model(self, request, image, form, change):
        if not change:
            image.created_by = request.user
        image.save()

admin.site.register(Language)
admin.site.register(Section, SectionAdmin)
admin.site.register(TransSection, TransSectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(TransArticle, TransArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(SectionImage, SectionImageAdmin)
