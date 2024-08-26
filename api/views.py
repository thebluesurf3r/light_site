# api/views.py
from rest_framework import generics
from rest_framework import viewsets
from .models import JobApplication
from .serializers import JobApplicationSerializer

class JobApplicationListCreate(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.request.query_params.get('organization', None)
        if organization:
            queryset = queryset.filter(organization__icontains=organization)
        return queryset
