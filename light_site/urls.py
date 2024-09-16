# light_site/urls.py
import logging
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, AboutView, ProjectView, ContactView

# Configure logging
logger = logging.getLogger(__name__)

# Base URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('project_structure/', include('project_structure.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Conditional logging and URL patterns for debug mode
if settings.DEBUG:
    logger.debug("Debug mode is enabled. Including debug toolbar URLs.")
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # Include debug toolbar URLs only in development
    ] + urlpatterns
else:
    logger.info("Debug mode is disabled. Debug toolbar URLs are not included.")

# Optionally, you can log the final URL patterns for debugging purposes
logger.debug("Final urlpatterns: %s", urlpatterns)
