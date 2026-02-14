from django.contrib import admin
from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'source_user', 'destination_user', 'course', 'create_date', 'update_date')
    list_filter = ('create_date', 'update_date', 'course')


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user', 'content', 'create_date', 'update_date')
    list_filter = ('create_date', 'chat')
