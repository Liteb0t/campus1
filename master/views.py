from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from master.models import Job, LineManager, Submission, Student, Recruiter
from master.serialisers import DBAdminStudentSerialiser, DBAdminSubmissionSerialiser, DBAdminJobSerialiser, DBAdminLineManagerSerialiser, UserSerialiser
from master.forms import StudentCreationForm, StudentUpdateForm, UserCreationForm
# from django.db.models import Q # for complex search lookups
# from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
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
def user_profile(request):
    Users_JSON = UserSerialiser(User.objects.all(), many = True).data
    return render(request, "user_profile.html", { "UsersJSON": json.dumps(Users_JSON)})

@login_required
def access_db_admin(request):
    return render(request, "db_view/access_db_admin.html")

# JSON API: does not return html but JSON instead. used by the new admin page.
# We need to make this secure later.
@csrf_exempt
def studentList(request):
    if request.method == "GET":
        students = Student.objects.select_related("user")
        students_serialiser = DBAdminStudentSerialiser(students, many=True)
        return JsonResponse(students_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = DBAdminStudentSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Student.objects.get(id=entry_id)
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        elif serialiser.is_valid(raise_exception=ValueError):
            if data["_action"] == "create":
                serialiser.create(validated_data=data)
            elif data["_action"] == "update":
                # instance = Student.objects.get(user=User.objects.get(id=data["_id"]))
                instance = Student.objects.get(id=data["_id"])
                serialiser.update(instance=instance, validated_data=data)
            # elif data["_action"] == "deleteMultiple":
            #     for entry_id in data["to_delete"]:
            #         instance = Student.objects.get(id=entry_id)
            #         serialiser.delete(instance=instance)
            return JsonResponse(serialiser.data, status=201)
        else:
            return JsonResponse(serialiser.errors, status=400)

# investigate why submissions take much longer to load than the rest
@csrf_exempt
def submissionList(request):
    if request.method == "GET":
        submissions = Submission.objects.select_related("student", "job", "line_manager")
        submissions_serialiser = DBAdminSubmissionSerialiser(submissions, many=True)
        return JsonResponse(submissions_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Submission.objects.get(id=entry_id)
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        if data["_action"] == "create":
            serialiser = DBAdminSubmissionSerialiser(data=data)
            if serialiser.is_valid(raise_exception=ValueError):
                serialiser.create(validated_data=data)
        elif data["_action"] == "update":
            instance = Submission.objects.get(id=data["_id"])
            print(data)
            # if data["student"]["id"] != instance.student.id:
            # data["student"] = Student.objects.get(id=data["student"]["id"]).__dict__
            # data["student"] = data["student"]["id"]
            print(data)
            serialiser = DBAdminSubmissionSerialiser(data=data)
            if serialiser.is_valid(raise_exception=ValueError):
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        else:
            return JsonResponse(serialiser.errors, status=400)
@csrf_exempt
def jobList(request):
    if request.method == "GET":
        jobs = Job.objects.all()
        jobs_serialiser = DBAdminJobSerialiser(jobs, many=True)
        return JsonResponse(jobs_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = DBAdminJobSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Job.objects.get(id=entry_id)
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        elif serialiser.is_valid(raise_exception=ValueError):
            if data["_action"] == "create":
                serialiser.create(validated_data=data)
            elif data["_action"] == "update":
                instance = Job.objects.get(id=data["_id"])
                serialiser.update(instance=instance, validated_data=data)
            return JsonResponse(serialiser.data, status=201)
        else:
            return JsonResponse(serialiser.errors, status=400)
@csrf_exempt
def lineManagerList(request):
    if request.method == "GET":
        linemanagers = LineManager.objects.all()
        linemanagers_serialiser = DBAdminLineManagerSerialiser(linemanagers, many=True)
        return JsonResponse(linemanagers_serialiser.data, safe=False)

@csrf_exempt
def currentUser(request):
    if request.method == "GET":
        users = [request.user]
        users_serialiser = UserSerialiser(users, many=True)
        return JsonResponse(users_serialiser.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = UserSerialiser(data=data)
        if serialiser.is_valid(raise_exception=ValueError):
            if data["_action"] == "create":
                serialiser.create(validated_data=data)
            elif data["_action"] == "update":
                # instance = Student.objects.get(user=User.objects.get(id=data["_id"]))
                instance = User.objects.get(id=data["_id"])
                serialiser.update(instance=instance, validated_data=data)
            elif data["_action"] == "delete":
                    serialiser.delete(instance=User.objects.get(id=data["_id"]))
            return JsonResponse(serialiser.data, status=201)
        else:
            return JsonResponse(serialiser.errors, status=400)
