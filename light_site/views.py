#light_site/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.utils import timezone
import pytz
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomAuthenticationForm
from django.views.generic import TemplateView
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ProjectView(TemplateView):
    template_name = 'projects.html'

class ContactView(TemplateView):
    template_name = 'contact.html'


@csrf_exempt
def call_flask_app(request):
    # URL of the Flask app
    flask_url = "http://127.0.0.1:5000"  
    response = requests.get(flask_url)
    return HttpResponse(response.text)