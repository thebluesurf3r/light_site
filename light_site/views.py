# light_site/views.py
import logging
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
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        logger.info(f"HomeView accessed by {request.user} at {request.path}")
        response = super().get(request, *args, **kwargs)
        logger.info(f"HomeView response status: {response.status_code}")
        return response

class AboutView(TemplateView):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        logger.info(f"AboutView accessed by {request.user} at {request.path}")
        response = super().get(request, *args, **kwargs)
        logger.info(f"AboutView response status: {response.status_code}")
        return response

class ProjectView(TemplateView):
    template_name = 'projects.html'

    def get(self, request, *args, **kwargs):
        logger.info(f"ProjectView accessed by {request.user} at {request.path}")
        response = super().get(request, *args, **kwargs)
        logger.info(f"ProjectView response status: {response.status_code}")
        return response

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        logger.info(f"ContactView accessed by {request.user} at {request.path}")
        response = super().get(request, *args, **kwargs)
        logger.info(f"ContactView response status: {response.status_code}")
        return response

@csrf_exempt
def call_flask_app(request):
    # URL of the Flask app
    flask_url = "http://127.0.0.1:5000"
    
    logger.info(f"Attempting to call Flask app at {flask_url}")

    try:
        response = requests.get(flask_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Received response from Flask app: Status Code {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while calling Flask app: {e}")
        return HttpResponse("Error connecting to Flask app.", status=500)
    
    # Log the content length for additional visibility
    content_length = len(response.text)
    logger.info(f"Response content length: {content_length} characters")

    return HttpResponse(response.text)
