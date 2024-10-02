# dir_scan/apps.py
import logging
from django.apps import AppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectStructureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dir_scan'

    def ready(self):
        """
        Override this method to perform initialization when the application is ready.
        """
        super().ready()
        logger.info(f"Application '{self.name}' is ready with default_auto_field set to '{self.default_auto_field}'")