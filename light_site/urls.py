# light_site/urls.py
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from .views import call_flask_app

from .views import HomeView, AboutView, ProjectView, ContactView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('project_structure/', include('project_structure.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # Include debug toolbar URLs only in development
    ] + urlpatterns
