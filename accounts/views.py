# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def signup(request):
    """
    Handle user sign-up by rendering a form and processing form submissions.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after sign-up
            auth_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('profile')  # Redirect to profile or any other desired page
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Handle user login by rendering a login form and processing authentication.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # Redirect to next parameter if exists, else to profile
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.
    """
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'accounts/logout.html')


@login_required
def profile(request):
    """
    Display user profile information.
    """
    return render(request, 'accounts/profile.html')
