from django import forms
from django.contrib.auth.forms import AuthenticationForm
import logging

# Set up logging
logger = logging.getLogger('myapp')  # Use your custom logger

class BaseForm(forms.Form):
    class Media:
        css = {
            "screen": ["pretty.css"],
            "tv,projector": ["lo_res.css"],
            "print": ["newspaper.css"],
        }
        js = ['/home/tron/git/light_site/static/js/script.js']

class CalendarDateInput(forms.DateInput):
    """
    A custom widget for date input with calendar popup.
    """
    input_type = 'date'
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'placeholder': 'YYYY-MM-DD'})
        super().__init__(*args, **kwargs)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        required=False  # Example to make it optional; adjust as needed
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and log the initialization.
        """
        super().__init__(*args, **kwargs)
        logger.info("CustomAuthenticationForm initialized with arguments: %s", args)
        logger.info("CustomAuthenticationForm initialized with keyword arguments: %s", kwargs)

    def clean(self):
        """
        Clean the form data and log the cleaning process.
        """
        logger.info("Cleaning form data...")
        cleaned_data = super().clean()
        # Add any additional cleaning or logging here if needed
        return cleaned_data

    def is_valid(self):
        """
        Check if the form is valid and log the validation status.
        """
        valid = super().is_valid()
        logger.info("Form is valid: %s", valid)
        return valid
