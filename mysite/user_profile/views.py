from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import Profile
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.forms import User
from . forms import UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy


@login_required
def profile(request):
    return render(request, 'user_profile/profile.html')


@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('User profile was updated succeefully'))
            return redirect(reverse_lazy('profile'))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_error = False
        if not username or get_user_model().objects.filter(username=username).exists():
            messages.error(request, _('Username already exists or was not entered.'))
            is_error = True
        if not first_name or not last_name:
            messages.error(request, _('First_name or second_name were not entered'))
            is_error = True
        if not email or get_user_model().objects.filter(email=email).exists():
            messages.error(request, _('User with this email address already exists, or email was entered incorrectly.'))
            is_error = True
        if not password or not password2 or password != password2:
            messages.error(request, _('Passwords do not match or were not entered.'))
            is_error = True
        if is_error:
            return redirect('register')
        else:
            get_user_model().objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            messages.success(request, _('User {} was created successfully.').format(username))
            return redirect('login')
    else:
        return render(request, 'user_profile/register.html')
