from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProgrammerCreationForm, ProgrammerLoginForm

# Create your views here.

def index(request):
	return render(request, 'base.html')

def login(request):
	if request.method == 'POST':
		pass
	login_form = ProgrammerLoginForm()
	return render(request, 'users/login.html', {'form': login_form})

@login_required
def logout(request):
	logout(request)
	return redirect(reverse('login'))

def sign_up(request):
	creation_form = ProgrammerCreationForm()
	return render(request, 'users/sign_up.html', {'form': creation_form})