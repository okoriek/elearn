from django import forms
from . models import Account, Assignment
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'gender','courses', 'phone_number')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('result_url', 'lesson', 'github_url')