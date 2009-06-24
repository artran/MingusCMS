from django.contrib import admin
from mingus.models import *

class ArticleImageInline(admin.StackedInline):
    model = ArticleImage

class SectionImageInline(admin.StackedInline):
    model = SectionImage

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
    list_display = ('title', 'live_from', 'live_to', 'is_live')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ArticleImageInline,)
    filter_horizontal = ('related',)

class TransArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'lang')
    list_filter = ['lang']

class ArticleImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SectionImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Language)
admin.site.register(Section, SectionAdmin)
admin.site.register(TransSection, TransSectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(TransArticle, TransArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(SectionImage, SectionImageAdmin)
