# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, OperatorProfile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to dashboard
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('accounts:login')
    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        # Update basic info
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        # If operator, update operator profile
        if user.role == 'operator':
            profile = getattr(user, 'operator_profile', None)
            if profile:
                profile.assigned_toll_point = request.POST.get("assigned_toll_point")
                profile.contact_number = request.POST.get("contact_number")
                profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    context = {}
    if user.role == 'operator':
        context['profile'] = getattr(user, 'operator_profile', None)

    context['user'] = user
    return render(request, "accounts/profile.html", context)
