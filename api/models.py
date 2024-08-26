# api/models.py
from django.db import models

class JobApplication(models.Model):
    organization = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    date_of_application = models.DateField()
    time_of_application = models.CharField(max_length=255)  # Update this field type if needed
    designation = models.CharField(max_length=255)

    class Meta:
        db_table = 'applications'  # Explicitly use the existing 'applications' table
        

