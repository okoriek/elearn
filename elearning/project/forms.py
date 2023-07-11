from django import forms
from . models import Account
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'gender', 'phone_number')