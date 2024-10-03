# light_site/urls.py

import logging
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, AboutView, ProjectView, ContactView
from django_plotly_dash import DjangoDash
from django_plotly_dash import urls as plotly_dash_urls
from dir_scan_vis.views import DashAppView


# Configure logging
logger = logging.getLogger(__name__)

# Base URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_management/', include('user_management.urls')),
    path('dir_scan/', include('dir_scan.urls')),
    path('dir_scan_vis/', include('dir_scan_vis.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('django_plotly_dash/', include(plotly_dash_urls)),  # Include Django Dash URLs
]

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
