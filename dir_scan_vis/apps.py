from django.apps import AppConfig

class DirScanVisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dir_scan_vis'

    def ready(self):
        from .dash_app import app