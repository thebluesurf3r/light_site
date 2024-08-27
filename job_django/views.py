from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

import pytz

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('thank_you')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def thank_you_view(request):
    return render(request, 'registration/thank_you.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Logged in as {user.username}")
            return redirect('profile')  # Redirect to the profile page or a different page if needed
        else:
            # Debugging: Output form errors to the console
            print("Form errors:", form.errors)
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
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

    context = {
        'user': user,
        'days_since_last_login': days_since_last_login,
        'time_of_last_login': last_login_ist,
        'time_of_current_login': current_time_ist,
    }
    return render(request, 'profile.html', context)

