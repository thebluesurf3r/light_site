# project_structure/models.py
import logging
from django.db import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectEntity(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('file', 'File'),
        ('directory', 'Directory'),
    ]

    entity_name = models.CharField(max_length=255)
    relative_path = models.CharField(max_length=500)
    level = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=ENTITY_TYPE_CHOICES)

    def __str__(self):
        return f'{self.entity_name} (Level: {self.level}, Type: {self.type})'

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
