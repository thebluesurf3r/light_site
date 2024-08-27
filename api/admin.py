#api/admin.py
from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the JobApplication model.
    """
    list_display = ('organization', 'job_location', 'date_of_application', 'time_of_application', 'designation')
    search_fields = ('organization', 'job_location', 'designation')
    list_filter = ('date_of_application', 'job_location')
