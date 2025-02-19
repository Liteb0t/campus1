from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from master.models import Job, LineManager, Submission, Student
# from django.db.models import Q # for complex search lookups
from django.template import loader
from .forms import AddStudentForm

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
    jobs = Job.objects.all()
    students = Student.objects.all()
    submissions = Submission.objects.all()
    line_managers = LineManager.objects.all()
    return render(request, "db_view/access_db_admin.html", {"Jobs": jobs, "Students": students, "Submissions": submissions, "LineManagers": line_managers})

def access_db_student(request):
    submissions = Submission.objects.all()
    valid_search_parameters = ["hours", "student_id"]
    for search_parameter in valid_search_parameters:
        if request.GET.__contains__(search_parameter):
            # submissions = submissions.filter(search_parameter=request.GET[search_parameter])
            submissions = submissions.filter(**{search_parameter: request.GET[search_parameter]})
    return render(request, "db_view/access_db_student.html", {"Submissions": submissions, "ValidSearchParameters": valid_search_parameters})

def add_student_form(request):
    context = {}
    context['form'] = AddStudentForm()
    return render(request, "access_db_admin.html", context)
