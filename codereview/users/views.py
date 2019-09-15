from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'base.html')

def log_in(request):
    return render(request, 'users/login.html')

@login_required
def log_out(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def sign_up(request):
    return render(request, 'users/sign_up.html')
