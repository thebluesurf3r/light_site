#job_django/urls.py
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings

from .views import SignUpView, ThankYouView, CustomLoginView, UserProfileView, HomeView, AboutView, ProjectView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('thank_you/', ThankYouView.as_view(), name='thank_you'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),


    ] + urlpatterns