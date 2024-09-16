from django.db import models

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