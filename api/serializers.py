from rest_framework import serializers
from .models import JobApplication

class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobApplication model.
    This serializer automatically includes all fields from the model.
    """
    class Meta:
        model = JobApplication
        fields = '__all__'
