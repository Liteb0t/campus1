from django.db import models
from django.contrib.auth.models import AbstractUser, User
from rest_framework import serializers
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
    accepted = models.BooleanField()

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Recruiter_Submission(models.Model):
    hours = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.BooleanField()

class DBAdminStudentSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'on_visa']

class DBAdminSubmissionSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(source='student.user.username', read_only=True)
    first_name = serializers.CharField(source='student.user.first_name', read_only=True)
    last_name = serializers.CharField(source='student.user.last_name', read_only=True)
    job_name = serializers.CharField(source='job.job_name', read_only=True)
    line_manager_username = serializers.CharField(source='line_manager.user.username', read_only=True)
    class Meta:
        model = Submission
        fields = ['username', 'first_name', 'last_name', 'job_name', 'line_manager_username', 'hours', 'date_worked', 'date_submitted', 'accepted']