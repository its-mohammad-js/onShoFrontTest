from django.urls import path

from . import views

urlpatterns = [
    path('chat/create', views.CreateChatAPI.as_view(), name='create-chat'),
    path('message/send', views.SendMessageAPI.as_view(), name='send-message'),
    path('chat/list', views.ChatListView.as_view(), name='list-chat'),
    path('chat/detail', views.ChatDetailView.as_view(), name='detail-chat'),
]
