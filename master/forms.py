from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
