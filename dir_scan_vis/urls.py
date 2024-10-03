# dir_scan_vis/urls.py

import logging
from django.urls import path, include
from .views import DashAppView, GraphView

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define URL patterns
urlpatterns = [
    path('', DashAppView.as_view(), name='dash_app_view'),
    path('graph/', GraphView.as_view(), name='graph_view'),
]

# Log URL pattern registration
logger.info(f"URL patterns have been registered for dir_scan_vis")