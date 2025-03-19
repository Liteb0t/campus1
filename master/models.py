from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    on_visa = models.BooleanField(default=False)
    visa_expiry = models.DateField(null=True)

class LineManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)

class Job(models.Model):
    job_name = models.CharField(max_length=255)
    cost_code = models.CharField(max_length=255)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    student = models.ManyToManyField(Student)

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    line_manager = models.ForeignKey(LineManager, on_delete=models.CASCADE)
    hours = models.IntegerField()
    date_worked = models.DateField()
    date_submitted = models.DateField()
    accepted = models.BooleanField(null=True)

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Recruiter_Submission(models.Model):
    hours = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.BooleanField(null=True)
