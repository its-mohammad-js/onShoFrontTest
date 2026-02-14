from django.urls import path
from .views import CourseImportView

urlpatterns = [
    path('import/', CourseImportView.as_view(), name='course-import'),
]
