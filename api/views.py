#api/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from .models import JobApplication
from .serializers import JobApplicationSerializer
from .filters import JobApplicationFilter


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the JobApplication model.
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    filterset_class = JobApplicationFilter


class JobApplicationListCreate(generics.ListCreateAPIView):
    """
    A generic view that provides GET (list) and POST (create) methods
    for the JobApplication model.
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
