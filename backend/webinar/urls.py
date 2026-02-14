from django.urls import path

from .views import WebinarListView, WebinarDetailView

urlpatterns = [
    path('list', WebinarListView.as_view(), name='webinar-list'),  # برای لیست وبینارها
    path('detail', WebinarDetailView.as_view(), name='webinar-detail'),  # برای جزئیات وبینار
]
