#api/filters.py
import django_filters

from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):
    organization = django_filters.CharFilter(lookup_expr='icontains')
    # Add more filters here as needed

    class Meta:
        model = JobApplication
        fields = ['organization']
