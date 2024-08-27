#api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, JobApplicationListCreate

router = DefaultRouter()
router.register(r'jobapplications', JobApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('jobapplications/list-create/', JobApplicationListCreate.as_view(), name='jobapplication-list-create'),
]
