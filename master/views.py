from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from master.models import Job, LineManager, Submission, Student
from master.forms import StudentCreationForm
# from django.db.models import Q # for complex search lookups
from django.template import loader
from django.core.paginator import Paginator

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

    if request.GET.__contains__("Jobs_page"):
        jobs_page_number = request.GET.get("Jobs_page")
    else:
        jobs_page_number = 1
    jobs_paginator = Paginator(jobs, 20)
    jobs_page_obj = jobs_paginator.get_page(jobs_page_number)

    if request.GET.__contains__("Students_page"):
        students_page_number = request.GET.get("Students_page")
    else:
        students_page_number = 1
    students_paginator = Paginator(students, 20)
    students_page_obj = students_paginator.get_page(students_page_number)

    if request.GET.__contains__("Submissions_page"):
        submissions_page_number = request.GET.get("Submissions_page")
    else:
        submissions_page_number = 1
    submissions_paginator = Paginator(submissions, 20)
    submissions_page_obj = submissions_paginator.get_page(submissions_page_number)

    if request.GET.__contains__("LineManagers_page"):
        line_managers_page_number = request.GET.get("LineManagers_page")
    else:
        line_managers_page_number = 1
    line_managers_paginator = Paginator(line_managers, 20)
    line_managers_page_obj = line_managers_paginator.get_page(line_managers_page_number)

    message = None
    student_creation_form = StudentCreationForm()
    if request.method == "POST":
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            message = "Added student!"
        else:
            message = "Form invalid, Student not added!"

    return render(request, "db_view/access_db_admin.html", {"Jobs": jobs_page_obj, "Students": students_page_obj, "Submissions": submissions_page_obj, "LineManagers": line_managers_page_obj, "StudentCreationForm": student_creation_form, "Message": message})

def access_db_student(request):
    submissions = Submission.objects.all()
    valid_search_parameters = ["hours", "student_id"]
    for search_parameter in valid_search_parameters:
        if request.GET.__contains__(search_parameter):
            # submissions = submissions.filter(search_parameter=request.GET[search_parameter])
            submissions = submissions.filter(**{search_parameter: request.GET[search_parameter]})
    if request.GET.__contains__("Submissions_page"):
        submissions_page_number = request.GET.get("Submissions_page")
    else:
        submissions_page_number = 1
    submissions_paginator = Paginator(submissions, 20)
    submissions_page_obj = submissions_paginator.get_page(submissions_page_number)
    return render(request, "db_view/access_db_student.html", {"Submissions": submissions_page_obj, "ValidSearchParameters": valid_search_parameters})

