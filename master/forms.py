from django.contrib.auth.forms import UserCreationForm
from master.models import Student


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + ("on_visa",)
