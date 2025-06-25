from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import registrationform
from .models import DjangoUserProfile


# 🔹 Registration view (original code)
def register(request):
    if request.method == 'POST':
        form = registrationform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Optional: Auto-login after registration
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)

            messages.info(request, f'Hello {username}, You are Successfully Registered!!') 
            return render(request, 'success.html')

    else:
        form = registrationform()
    return render(request, 'register.html', {'form': form})


# 🔹 Dashboard view with role-based access
@login_required
def dashboard(request):
    try:
        profile = DjangoUserProfile.objects.get(user=request.user)
    except DjangoUserProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Your role profile is not set. Please contact admin.'})

    # ✅ Admin: Can see all users
    if profile.role and profile.role.role_name == 'admin':
        data = User.objects.all()
        access = 'full'
    else:
        # ✅ Normal users: Can only see their own data
        data = User.objects.filter(username=request.user.username)
        access = 'view-only'

    return render(request, 'dashboard.html', {
        'data': data,
        'role': profile.role.role_name if profile.role else 'No Role',
        'access': access
    })
