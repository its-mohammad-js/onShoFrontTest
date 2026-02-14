from django.contrib import admin
from .models import StaticContent, RelatedLink
from ckeditor.widgets import CKEditorWidget
from django import forms


class StaticContentAdminForm(forms.ModelForm):
    class Meta:
        model = StaticContent
        fields = '__all__'
        widgets = {
            'short_description': CKEditorWidget(config_name='default'),
            'description': CKEditorWidget(config_name='default'),
        }


class RelatedLinkInline(admin.TabularInline):
    model = RelatedLink
    extra = 1
    fields = ['title', 'description', 'url', 'external', 'order']
    ordering = ['order']


@admin.register(StaticContent)
class StaticContentAdmin(admin.ModelAdmin):
    form = StaticContentAdminForm
    list_display = ['title', 'category', 'display_order', 'slug', 'is_active', 'create_date', 'update_date']
    list_filter = ['category', 'is_active', 'create_date', 'update_date']
    search_fields = ['title', 'slug', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RelatedLinkInline]
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('title', 'slug', 'short_description', 'description', 'category', 'display_order', 'is_active')
        }),
    )


@admin.register(RelatedLink)
class RelatedLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'static_content', 'url', 'external', 'order', 'create_date']
    list_filter = ['external', 'static_content', 'create_date']
    search_fields = ['title', 'description', 'url']
    ordering = ['static_content', 'order']
