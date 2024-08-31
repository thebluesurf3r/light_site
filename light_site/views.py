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


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('thank_you')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully. Please log in.")
        return response

class ThankYouView(TemplateView):
    template_name = 'registration/thank_you.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        messages.success(self.request, f"Logged in as {user.username}")
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Invalid username or password.")
        return response

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        last_login = user.last_login
        current_time = timezone.now()

        # Define the IST timezone
        ist = pytz.timezone('Asia/Kolkata')

        # Convert times to IST
        if last_login:
            last_login_ist = last_login.astimezone(ist)
            days_since_last_login = (current_time - last_login).days
        else:
            last_login_ist = "N/A"
            days_since_last_login = "N/A"  # Handle case where last_login is None

        current_time_ist = current_time.astimezone(ist)

        context.update({
            'days_since_last_login': days_since_last_login,
            'time_of_last_login': last_login_ist,
            'time_of_current_login': current_time_ist,
        })
        return context

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ProjectView(TemplateView):
    template_name = 'projects.html'

class ContactView(TemplateView):
    template_name = 'contact.html'