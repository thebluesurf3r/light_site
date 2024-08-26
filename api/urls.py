# api/urls.py
from django.urls import path
from .views import JobApplicationListCreate, JobApplicationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'job-applications', JobApplicationViewSet, basename='job-application')

urlpatterns = [
    path('', JobApplicationListCreate.as_view(), name='job-application-list-create'),
] + router.urls
