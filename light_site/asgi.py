#light_site/asgi.py
import os
import logging

from django.core.asgi import get_asgi_application

# Set up logging
logger = logging.getLogger('myapp')  # Use your custom logger

def setup_logging():
    """
    Configure logging for ASGI application.
    """
    logger.info("Setting up ASGI application...")

# Ensure the DJANGO_SETTINGS_MODULE is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'light_site.settings')

# Log the application initialization
setup_logging()
logger.info("ASGI application setup complete.")

application = get_asgi_application()
