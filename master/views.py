from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from master.models import Job, LineManager, Submission, Student
# from django.db.models import Q # for complex search lookups
from django.template import loader
from django.core.paginator import Paginator
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
    if request.GET.__contains__("page"):
        page_number = request.GET.get("page")
    else:
        page_number = 1
    paginator = Paginator(jobs, 25)
    page_obj_job = paginator.get_page(page_number)
    paginator = Paginator(students, 25)
    page_obj_stu = paginator.get_page(page_number)
    paginator = Paginator(LineManager, 25)
    page_obj_man = paginator.get_page(page_number)
    paginator = Paginator(submissions, 25)
    page_obj_sub = paginator.get_page(page_number)
    return render(request, "db_view/access_db_admin.html", {"Jobs": page_obj_job, "Students": page_obj_stu, "Submissions": page_obj_sub, "LineManagers": page_obj_man})

def access_db_student(request):
    submissions = Submission.objects.all()
    valid_search_parameters = ["hours", "student_id"]
    for search_parameter in valid_search_parameters:
        if request.GET.__contains__(search_parameter):
            # submissions = submissions.filter(search_parameter=request.GET[search_parameter])
            submissions = submissions.filter(**{search_parameter: request.GET[search_parameter]})
    if request.GET.__contains__("page"):
        page_number = request.GET.get("page")
    else:
        page_number = 1
    paginator = Paginator(submissions, 20)
    page_obj = paginator.get_page(page_number)
    return render(request, "db_view/access_db_student.html", {"Submissions": page_obj, "ValidSearchParameters": valid_search_parameters})

def add_student_form(request):
    student_id = request.POST["student_id"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    surname = request.POST["surname"]
    password = request.POST["password"]
