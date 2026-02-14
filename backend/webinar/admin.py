from django.contrib import admin

from .models import Webinar, WebinarTopic


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'date', 'start_time', 'end_time', 'price', 'is_free')
    list_filter = ('date', 'is_free')
    search_fields = ('title', 'speaker', 'description')
    ordering = ('-date', 'start_time')


@admin.register(WebinarTopic)
class WebinarTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'webinar')
    search_fields = ('title', 'content')
    list_filter = ('webinar',)
