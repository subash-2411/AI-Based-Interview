from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import UserHistory
from .forms import StudentRegisterForm, StudentLoginForm, ProfileUpdateForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')  <-- Auto-login removed
            messages.success(request, f"Account created for {user.username}! Please login to continue.")
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    history, created = UserHistory.objects.get_or_create(user=request.user)
    skills = request.user.skills.all()
    
    context = {
        'history': history,
        'skills': skills,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'title': 'Edit Profile'
    })
