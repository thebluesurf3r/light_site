# project_structure/urls.py
import logging
from django.urls import path
from . import views

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define URL patterns
urlpatterns = [
    path('index/', views.index, name='index'),
    path('graphs/', views.graphs, name='graphs')
]

# Log URL pattern registration
logger.info(f"URL patterns have been registered for project_structure")