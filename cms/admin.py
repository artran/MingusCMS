from django.contrib import admin
from models import *

from datetime import datetime


class SectionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'sort', 'live')
    prepopulated_fields = {'slug': ('name',)}


class TransSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'lang')
    list_filter = ['lang']


class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ('section',)
    search_fields = ('title',)
    list_display = ('title', 'section', 'live_from', 'live_to', 'is_live')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('related',)


class TransArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'lang')
    list_filter = ['lang']


class ImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MediaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TextChunkAdmin(admin.ModelAdmin):
    pass


class PageTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language)
admin.site.register(Section, SectionAdmin)
admin.site.register(TransSection, TransSectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(TransArticle, TransArticleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(TextChunk, TextChunkAdmin)
admin.site.register(PageTemplate, PageTemplateAdmin)
