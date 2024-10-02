# dir_scan_vis/models.py

import logging
from django.db import models

# Configure logging
logger = logging.getLogger(__name__)

class ProjectEntity(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('file', 'File'),
        ('directory', 'Directory'),
    ]

    directory = models.CharField(max_length=500)
    filename = models.CharField(max_length=255)
    full_path = models.CharField(max_length=1000)
    file_size = models.BigIntegerField()
    metadata_change_time = models.DateTimeField()
    modification_time = models.DateTimeField()
    access_time = models.DateTimeField()
    file_age_in_days = models.IntegerField()
    meta_data_age_in_days = models.IntegerField()
    recently_accessed = models.BooleanField(default=False)
    file_size_category = models.CharField(max_length=500, blank=True, null=True)
    file_extension = models.CharField(max_length=100, blank=True, null=True)
    python_file = models.BooleanField(default=False)
    file_depth = models.IntegerField()
    django_element_type = models.CharField(max_length=100, blank=True, null=True)
    expected_location = models.BooleanField(default=False)
    hover_template = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.filename} (Path: {self.full_path}, Size: {self.file_size})'

    def save(self, *args, **kwargs):
        if self.pk:
            logger.info(f'Updating ProjectEntity: {self}')
        else:
            logger.info(f'Creating new ProjectEntity: {self}')
        super().save(*args, **kwargs)
        logger.info(f'ProjectEntity saved: {self}')

    def delete(self, *args, **kwargs):
        logger.info(f'Deleting ProjectEntity: {self}')
        super().delete(*args, **kwargs)
        logger.info(f'ProjectEntity deleted: {self}')