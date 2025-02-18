from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from master.models import Job, LineManager, Submission, Student
from django.template import loader

@login_required
def homepage(request):
    return render(request, "homepage.html")

def logged_out(request):
    return render(request, "registration/logged_out.html")

@login_required
def secure(request):
    return render(request, "secure.html")

def profile(request):
    return render(request, "profile.html")

def access_db_admin(request):
    Jobs = Job.objects.all()
    Students = Student.objects.all()
    Submissions = Submission.objects.all()
    LineManagers = LineManager.objects.all()
    return render(request, "db_view/access_db_admin.html", {"Jobs": Jobs,"Students": Students, "Submissions": Submissions,"LineManagers": LineManagers})

def access_db_student(request):
    Submissions = Submission.objects.all()
    return render(request, "db_view/access_db_student.html", {"Submissions" : Submissions})

