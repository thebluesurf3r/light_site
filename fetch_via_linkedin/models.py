from django.db import models

class ViaLinkedIn(models.Model):
    id = models.TextField()
    organization = models.TextField()
    designation = models.TextField()
    date_of_application = models.TextField()
    time_of_application = models.TextField()
    job_location = models.TextField()
    job_id = models.CharField(max_length=255)
    email_body = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'job_location', 'date_of_application', 'time_of_application'], name='unique_application'),
        ]

    def __str__(self):
        return f"{self.organization} - {self.designation} ({self.job_id})"