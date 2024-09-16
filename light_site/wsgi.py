# light_site/wsgi.py
import os
import logging

from django.core.wsgi import get_wsgi_application

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'light_site.settings')

logger.info('Starting WSGI application with settings module: %s', os.environ.get('DJANGO_SETTINGS_MODULE'))

# Create the WSGI application object
application = get_wsgi_application()

logger.info('WSGI application has been initialized.')