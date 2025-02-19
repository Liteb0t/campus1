from django import forms
from master.models import Student
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class AddStudentForm(forms.Form):
    student_id = forms.CharField()
    email = forms.CharField
    first_name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
