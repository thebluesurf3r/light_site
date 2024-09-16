from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery

# Set up logging
logger = logging.getLogger('myapp')  # Use your custom logger

def setup_logging():
    """
    Configure logging for the Celery setup.
    """
    logger.info("Starting Celery application setup...")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'light_site.settings')

setup_logging()

app = Celery('light_site')

# Configure Celery to use Django settings
logger.info("Configuring Celery with Django settings...")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
logger.info("Discovering Celery tasks...")
app.autodiscover_tasks()

# Configure Celery to use Django for storing task results
logger.info("Configuring Celery result backend...")
app.conf.result_backend = 'django-db'

logger.info("Celery application setup complete.")