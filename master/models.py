from django.db import models

# Create your models here.

class Job(models.Model):
    Job_Name = models.CharField(max_length=255)
    Cost_Code = models.CharField(max_length=255)
    Pay_Rate = models.DecimalField(max_digits=10, decimal_places=2)

class LineManager(models.Model):
    Name = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)

class Student(models.Model):
    Student_Payroll = models.IntegerField()
    Surname = models.CharField(max_length=255)
    First_Name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)

class Submission(models.Model):
    Student_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    Job_ID = models.ForeignKey(Job, on_delete=models.CASCADE)
    Line_Manager_ID = models.ForeignKey(LineManager, on_delete=models.CASCADE)
    Hours = models.IntegerField()
    Date_Worked = models.DateField()
    Date_Submitted = models.DateField()

