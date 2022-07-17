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

@login_required
def profile(request):
    return render(request, 'user_profile/profile.html')

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_error = False
        if not username or get_user_model().objects.filter(username=username).exists():
            messages.error(request, _('Username already exists or was not entered.'))
            is_error = True
        if not email or get_user_model().objects.filter(email=email).exists():
            messages.error(request, _('User with this email address already exists, or email was entered incorrectly.'))
            is_error = True
        if not password or not password2 or password != password2:
            messages.error(request, _('Passwords do not match or were not entered.'))
            is_error = True
        # try:
        #     validate_password(password, password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
        # except Exception as password_error:
        #     messages.error(request, _('Password error: {}').format(password_error[0]))
        #     is_error = True
        if is_error:
            return redirect('register')
        else:
            get_user_model().objects.create_user(username=username, email=email, password=password)
            messages.success(request, _('User {} was created successfully.').format(username))
            return redirect('login')
    else:
        return render(request, 'user_profile/register.html')