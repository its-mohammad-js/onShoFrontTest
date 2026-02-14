from django.urls import path
from . import views

urlpatterns = [
    path('list', views.StaticContentListView.as_view(), name='static_content_list'),
    path('detail', views.StaticContentDetailView.as_view(), name='static_content_detail'),
]

