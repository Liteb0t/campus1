from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils import timezone
import datetime

# Create your models here.
class CampusUserManager(BaseUserManager):

    def create_user(self, username, email, password=None,first_name=None, last_name=None, is_staff=False, is_superuser=False, user_type="Default"):
        if not email:
            raise ValueError('Cannot create a user without an email address ')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password, first_name, last_name, user_type):
        user = self.create_user(
            username,
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
        )
        # user.staff = True
        # user.admin = True
        user.user_type = user_type
        user.save(using=self._db)
        return user

class CampusUser(AbstractUser):
    objects = CampusUserManager()
    username = models.CharField(max_length=64, unique=True, null=True, default=None)
    email = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=16)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name','user_type']

class Student(models.Model):
    user = models.OneToOneField(CampusUser, on_delete=models.CASCADE)
    on_visa = models.BooleanField(default=False)
    eligible_to_work = models.BooleanField(default=False)
    visa_expiry = models.DateField(null=True)
    hours_worked = models.IntegerField(default=0)

class Recruiter(models.Model):
    user = models.OneToOneField(CampusUser, on_delete=models.CASCADE)

class LineManager(models.Model):
    user = models.OneToOneField(CampusUser, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

class Job(models.Model):
    job_name = models.CharField(max_length=255)
    cost_code = models.CharField(max_length=255)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    student = models.ManyToManyField(Student)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    line_manager = models.ForeignKey(LineManager, on_delete=models.CASCADE, null=True, blank=True)
    hours = models.IntegerField()
    date_worked = models.DateField()
    date_submitted = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    accepted = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
