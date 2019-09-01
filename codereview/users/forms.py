from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Programmer


class ProgrammerCreationForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = Programmer
		fields = ('email', 'github_account')


class ProgrammerLoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Programmer
		fields = ('email', 'password')
