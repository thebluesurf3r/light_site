#job_django/urls.py
from django.contrib import admin
from django.urls import path, include

from .views import signup_view, login_view, profile_view, thank_you_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('accounts/profile/', profile_view, name='profile'),
    path('thank-you/', thank_you_view, name='thank_you'),
]