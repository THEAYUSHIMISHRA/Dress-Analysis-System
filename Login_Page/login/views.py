from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from register.models import DjangoUserProfile  # Make sure this is correct

# 🔹 Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Hello {username}, You Are Successfully Logged In")
            return redirect('dashboard')  # 🔁 Go to dashboard on success
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username Doesn't Exist")
            else:
                messages.info(request, "Incorrect Password")
            return redirect('login')  # Stay on login page

    return render(request, "login.html")

# 🔹 Logout View
def logout_view(request):
    auth.logout(request)
    return redirect('login')

# 🔹 Dashboard View with Role-based Access
@login_required
def dashboard(request):
    try:
        profile = DjangoUserProfile.objects.get(user=request.user)
    except DjangoUserProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Your role profile is not set. Please contact admin.'})

    if profile.role and profile.role.role_name == 'admin':
        data = User.objects.all()  # Admin sees all
        access = 'full'
    else:
        data = [request.user]  # Normal user sees only themselves
        access = 'view-only'

    return render(request, 'dashboard.html', {
        'data': data,
        'role': profile.role.role_name if profile.role else 'No Role',
        'access': access
    })
