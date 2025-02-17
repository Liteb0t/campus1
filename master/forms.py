from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
