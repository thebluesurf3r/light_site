# dir_scan/urls.py
import logging
from django.urls import path, include
from . import views

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define URL patterns
urlpatterns = [
    path('', views.index, name='scan'),
]

# Log URL pattern registration
logger.info(f"URL patterns have been registered for dir_scan")