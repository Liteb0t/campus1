from django import forms


class Placeholders(forms.Form):
    username = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Password'}))
