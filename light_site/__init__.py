from __future__ import absolute_import, unicode_literals
import logging

# Set up logging
logger = logging.getLogger('myapp')  # Use your custom logger

def setup_logging():
    """
    Configure logging for the app initialization.
    """
    logger.info("Initializing Celery app...")

# Make sure the app is always imported when Django starts so that shared_task will use this app.
from .celery import app as celery_app

# Log the Celery app initialization
setup_logging()
logger.info("Celery app initialization complete.")

__all__ = ('celery_app',)