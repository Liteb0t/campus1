from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from master.models import Student
from django import forms
from django.db import models


class StudentCreationForm(forms.ModelForm):
    # username = forms.CharField(
    #     label="",
    #     strip=False,
    #     widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    #     help_text=None,
    # )
    #
    # email = forms.CharField(
    #     label="",
    #     strip=False,
    #     widget=forms.TextInput(attrs={'placeholder': 'Email'}),
    #     help_text=None,
    # )
    #
    # first_name = forms.CharField(
    #     label="",
    #     strip=False,
    #     widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    #     help_text=None,
    # )
    #
    # last_name = forms.CharField(
    #     label="",
    #     strip=False,
    #     widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    #     help_text=None,
    # )
    #
    # password1 = forms.CharField(
    #     label="",
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    #     help_text=None,
    # )
    # password2 = forms.CharField(
    #     label="",
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    #     strip=False,
    #     help_text=None,
    # )

    class Meta:
        model = Student
        fields = ["on_visa", "visa_expiry"]
        widgets = {
            "visa_expiry": forms.widgets.DateInput(attrs={'type': 'date'})
        }


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["on_visa", "visa_expiry"]
        widgets = {
            "visa_expiry": forms.widgets.DateInput(attrs={'type': 'date'})
        }
