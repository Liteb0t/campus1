from django import forms
from master.models import Student
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class AddStudentForm(forms.Form):
    student_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
