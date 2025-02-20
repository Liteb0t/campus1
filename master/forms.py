from django.contrib.auth.forms import UserCreationForm
from master.models import Student


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + ("on_visa", "first_name", "last_name", "email")
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
        }
