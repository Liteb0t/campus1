from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from master.models import Job, LineManager, Submission, Student, Recruiter, DBAdminStudentSerialiser ,DBAdminSubmissionSerialiser
from master.forms import StudentCreationForm, StudentUpdateForm, UserCreationForm
# from django.db.models import Q # for complex search lookups
from django.template import loader
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import redirect
import json

@login_required
def homepage(request):
    if request.user.is_superuser == 1:
        return render(request, "homepage.html")
    else:
        return redirect("student")

def logged_out(request):
    return render(request, "registration/logged_out.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def recruiter_profile(request):
    return render(request, "recruiter_profile.html")

@login_required
def admin_profile(request):
    return render(request, "admin_profile.html")

@login_required
def access_db_admin_old(request):
    jobs = Job.objects.all()
    recruiters = Recruiter.objects.all() #paginate this!
    students = Student.objects.all()
    submissions = Submission.objects.select_related("student", "job", "line_manager")
    line_managers = LineManager.objects.all()

    valid_search_parameters = [["hours", "text"], ["student__user__username", "text"], ["student__user__first_name", "text"],
                               ["student__user__last_name", "text"], ["date_worked", "date"], ["date_submitted", "date"]]
    for search_parameter in valid_search_parameters:
        if request.GET.__contains__(search_parameter[0]):
            # submissions = submissions.filter(search_parameter=request.GET[search_parameter])
            if search_parameter[1] == "date":
                delimiter = request.GET.get(search_parameter[0] + "-delimiter")

                ## Stuff delimiter conditional
                if delimiter == "At":
                    submissions = submissions.filter(**{search_parameter[0]: request.GET[search_parameter[0]]})
                elif delimiter == "Before":
                    submissions = submissions.filter(
                        **{search_parameter[0] + "__range": ["0001-01-01", request.GET[search_parameter[0]]]})
                # elif delimiter == "After":
                else:
                    submissions = submissions.filter(
                        **{search_parameter[0] + "__range": [request.GET[search_parameter[0]], "9999-12-31"]})
            else:
                submissions = submissions.filter(**{search_parameter[0]: request.GET[search_parameter[0]]})

    if request.GET.__contains__("Students_page"):
        students_page_number = request.GET.get("Students_page")
    else:
        students_page_number = 1
    students_paginator = Paginator(students, 20)
    students_page_obj = students_paginator.get_page(students_page_number)

    if request.GET.__contains__("Jobs_page"):
        jobs_page_number = request.GET.get("Jobs_page")
    else:
        jobs_page_number = 1
    jobs_paginator = Paginator(jobs, 20)
    jobs_page_obj = jobs_paginator.get_page(jobs_page_number)

    if request.GET.__contains__("LineManagers_page"):
        line_managers_page_number = request.GET.get("LineManagers_page")
    else:
        line_managers_page_number = 1
    line_managers_paginator = Paginator(line_managers, 20)
    line_managers_page_obj = line_managers_paginator.get_page(line_managers_page_number)

    if request.GET.__contains__("Submissions_page"):
        submissions_page_number = request.GET.get("Submissions_page")
    else:
        submissions_page_number = 1
    submissions_paginator = Paginator(submissions, 20)
    submissions_page_obj = submissions_paginator.get_page(submissions_page_number)

    message = None
    user_creation_form = UserCreationForm()
    student_creation_form = StudentCreationForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            message = "Added student!"
            if student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.save()

    return render(request, "db_view/access_db_admin_old.html", {"Jobs": jobs_page_obj, "Students": students_page_obj, "Submissions": submissions_page_obj, "LineManagers": line_managers_page_obj, "StudentCreationForm": student_creation_form, "UserCreationForm": user_creation_form, "ValidSearchParameters": valid_search_parameters, "Message": message})

@login_required
def access_db_admin(request):
    jobs = Job.objects.all()
    recruiters = Recruiter.objects.all() #paginate this!
    students = Student.objects.select_related("user")
    submissions = Submission.objects.select_related("student", "job", "line_manager")
    line_managers = LineManager.objects.all()

    message = None
    user_creation_form = UserCreationForm()
    student_creation_form = StudentCreationForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            message = "Added student!"
            if student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.save()

    submissions_pure = submissions.values("hours", "student__user__username")
    # students_pure = students.only("user__username", "on_visa")
    students_json = DBAdminStudentSerialiser(students, many=True).data
    submissions_json = DBAdminSubmissionSerialiser(submissions, many=True).data
    return render(request, "db_view/access_db_admin.html", {"StudentCreationForm": student_creation_form, "UserCreationForm": user_creation_form, "Message": message, "StudentsJSON": json.dumps(students_json), "SubmissionsJSON": json.dumps(submissions_json)})

@login_required
def updatestudent(request, id):
    stu_id = Student.objects.get(id=id)
    student_update_form = StudentUpdateForm(instance=stu_id)
    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=stu_id)
        if form.is_valid():
            form.save()
            return redirect("adminSHU")

    return render(request, "db_view/UpdateStudent.html", {"StudentUpdateForm": student_update_form})

@login_required
def deletestudent(request, id):
    stu_id = Student.objects.get(id=id)
    stu_id.delete()
    return redirect("adminSHU")

@login_required
def deletejob(request, id):
    Job_id = Job.objects.get(id=id)
    Job_id.delete()
    return redirect("adminSHU")

@login_required
def deletesubmission(request, id):
    sub_id = Submission.objects.get(id=id)
    sub_id.delete()
    return redirect("adminSHU")

@login_required
def access_db_student(request):
    submissions = Submission.objects.select_related("student").filter(student__username=request.user.username)
    valid_search_parameters = [[ "hours", "text"], ["date_worked", "date"], ["date_submitted", "date"]]
    for search_parameter in valid_search_parameters:
        if request.GET.__contains__(search_parameter[0]):
            # submissions = submissions.filter(search_parameter=request.GET[search_parameter])
            if search_parameter[1] == "date":
                delimiter = request.GET.get(search_parameter[0] + "-delimiter")

                ## Stuff delimiter conditional
                if delimiter == "At":
                    submissions = submissions.filter(**{search_parameter[0]: request.GET[search_parameter[0]]})
                elif delimiter == "Before":
                    submissions = submissions.filter(**{search_parameter[0] + "__range": ["0001-01-01", request.GET[search_parameter[0]]]})
                # elif delimiter == "After":
                else:
                    submissions = submissions.filter(**{search_parameter[0] + "__range": [request.GET[search_parameter[0]], "9999-12-31"]})
            else:
                submissions = submissions.filter(**{search_parameter[0]: request.GET[search_parameter[0]]})
    if request.GET.__contains__("Submissions_page"):
        submissions_page_number = request.GET.get("Submissions_page")
    else:
        submissions_page_number = 1
    # if request.GET.__contains__("worked_delimiter"):
    #     worked_delimiter = request.GET.get("worked_delimiter")
    submissions_paginator = Paginator(submissions, 20)
    submissions_page_obj = submissions_paginator.get_page(submissions_page_number)
    return render(request, "db_view/access_db_student.html", {"Submissions": submissions_page_obj, "ValidSearchParameters": valid_search_parameters})
