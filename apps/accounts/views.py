# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
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
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)

        # Handle password change if provided
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        if new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request, "New password and confirmation do not match")
                return redirect('accounts:profile')
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long")
                return redirect('accounts:profile')
            user.set_password(new_password)
            # Do not store plain passwords

        user.save()

        # If operator, update or create operator profile
        if user.role == 'operator':
            profile = getattr(user, 'operator_profile', None)
            if profile is None:
                profile = OperatorProfile.objects.create(user=user)
            profile.assigned_toll_point = request.POST.get("assigned_toll_point", profile.assigned_toll_point)
            profile.contact_number = request.POST.get("contact_number", profile.contact_number)
            profile.save()

        # Keep session valid after password change
        if new_password:
            update_session_auth_hash(request, user)

        messages.success(request, "Profile updated successfully")
        return redirect('accounts:profile')

    context = {}
    if user.role == 'operator':
        context['profile'] = getattr(user, 'operator_profile', None)

    context['user'] = user
    return render(request, "dashbaord/admin/profile.html", context)
