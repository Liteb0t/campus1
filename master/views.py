from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from master.models import Job, LineManager, Submission, Student, Recruiter # , RecruiterSubmission
from master.serialisers import DBAdminStudentSerialiser, DBAdminSubmissionSerialiser, DBAdminJobSerialiser, DBAdminJobDetailSerialiser, DBAdminLineManagerSerialiser, DBAdminLineManagerDetailSerialiser, UserSerialiser, DBAdminRecruiterSerialiser, DBAdminRecruiterDetailSerialiser, CampusUser, DBAdminSubmissionStudentSerialiser # , RecruiterSubmissionSerialiser
from rest_framework.response import Response
from master.forms import StudentCreationForm, StudentUpdateForm, UserCreationForm
# from django.db.models import Q # for complex search lookups
# from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
from django.shortcuts import redirect
import json
import datetime

duplicate_username_message = "Username may not be a duplicate"

@login_required
def homepage(request):
    if request.user.user_type == "Student":
        user = Student.objects.get(user__id=request.user.id)
    elif request.user.user_type == "Recruiter":
        user = Recruiter.objects.get(user__id=request.user.id)
    elif request.user.user_type == "LineManager":
        user = LineManager.objects.get(user__id=request.user.id)
    elif request.user.user_type == "Admin":
        user = request.user
    return render(request, "homepage.html", {"user": user})

def logged_out(request):
    return render(request, "registration/logged_out.html")

def deletedAccount(request):
    return render(request, "registration/deleted_account.html")

@login_required
def userProfile(request):
    Users_JSON = UserSerialiser(CampusUser.objects.all(), many = True).data
    return render(request, "user_profile.html", { "UsersJSON": json.dumps(Users_JSON)})

@login_required
def makesubmissionpage(request):
    student_id = Student.objects.get(user__id=request.user.id).id
    jobs = Job.objects.all()
    line_managers = LineManager.objects.all()
    return render(request, "MakeSubmission.html", {"StudentID": student_id, "Jobs": jobs, "Managers": line_managers})

@login_required
def accessDataBrowser(request):
    if (request.user.is_superuser):
        return render(request, "db_view/access_data_browser.html")
    else:
        return HttpResponse("You need to be an admin to access this page.", status=403)

@login_required
def accessStudentSubmission(request):
    student = Student.objects.get(user=request.user)
    return render(request, "db_view/access_student_submission.html", {"student": student})

@login_required
def accessRecruiterSubmission(request):
    return render(request, "db_view/access_recruiter_submission.html", {"job_read_only": request.user.user_type=="LineManager"})

@login_required
def accessManagerApproval(request):
    if request.user.user_type == "LineManager":
        line_manager_id = LineManager.objects.get(user=request.user).id
        return HttpResponseRedirect("/access_recruiter_submission?tsub_Line_manager_ID="+str(line_manager_id))
    else:
        return render(request, "db_view/access_recruiter_submission.html")

# JSON API: does not return html but JSON instead. used by the data browser.
@csrf_exempt
def studentList(request):
    if request.user.user_type not in ["Admin", "LineManager", "Recruiter"]: # only these user types can get a list of all students
        return JsonResponse({"message": "Not authorised"}, status=401)
    if request.method == "GET":
        students = Student.objects.select_related("user")
        students_serialiser = DBAdminStudentSerialiser(students, many=True)
        return JsonResponse(students_serialiser.data, safe=False)

    elif request.method == "POST":
        if request.user.user_type != "Admin": # only Admin can edit students
            return JsonResponse({"message": "Not authorised"}, status=401)
        data = JSONParser().parse(request)
        serialiser = DBAdminStudentSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Student.objects.get(id=entry_id)
                instance.user.delete()
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        elif data["_action"] == "create":
            username_equivalent = Student.objects.filter(user__username=data["user"]["username"])
            if username_equivalent.exists():
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = {}
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.create(validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                print(serialiser.errors)
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "update":
            instance = Student.objects.get(id=data["_id"])
            if "password" not in data["user"] or data["user"]["password"] == "":
                data["user"]["password"] = instance.user.password
            username_equivalent = CampusUser.objects.filter(username=data["user"]["username"])
            if (username_equivalent.exists() and username_equivalent[0].id != instance.user.id):
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = None
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        else:
            return JsonResponse(serialiser.errors, status=400)

@api_view(["GET"])
def studentDetail(request, pk):
    if request.method == "GET":
        student = Student.objects.get(id=pk)
        student_serialiser = DBAdminStudentSerialiser(student, many=False)
        return Response(student_serialiser.data)

@csrf_exempt
def submissionList(request):
    if request.method == "GET":
        submissions = Submission.objects.select_related("student", "job", "line_manager")
        if request.user.user_type == "Recruiter":
            submissions = submissions.filter(job__recruiter__user=request.user)
        elif request.user.user_type == "LineManager":
            line_manager = LineManager.objects.get(user=request.user)
            submissions = submissions.filter(job__recruiter=line_manager.recruiter)
        submissions_serialiser = DBAdminSubmissionSerialiser(submissions, many=True)
        return JsonResponse(submissions_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = DBAdminSubmissionSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Submission.objects.get(id=entry_id)
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        if data["_action"] == "create":
            if serialiser.is_valid():
                serialiser.create(validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "update":
            instance = Submission.objects.get(id=data["_id"])
            if serialiser.is_valid():
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        else:
            return JsonResponse(serialiser.errors, status=400)

@api_view(["GET"])
def submissionDetail(request, pk):
    submission = Submission.objects.get(id=pk)
    if request.method == "GET":
        submission_serialiser = DBAdminSubmissionSerialiser(submission);
        return Response(submission_serialiser.data)

@csrf_exempt
def recruiterList(request):
    if request.method == "GET":
        recruiters = Recruiter.objects.select_related("user")
        recruiters_serialiser = DBAdminRecruiterSerialiser(recruiters, many=True)
        return JsonResponse(recruiters_serialiser.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = DBAdminRecruiterSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = Recruiter.objects.get(id=entry_id)
                instance.user.delete()
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        elif data["_action"] == "create":
            username_equivalent = Recruiter.objects.filter(user__username=data["user"]["username"])
            if username_equivalent.exists():
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = {}
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.create(validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "update":
            instance = Recruiter.objects.get(id=data["_id"])
            if "password" not in data["user"] or data["user"]["password"] == "":
                data["user"]["password"] = instance.user.password
            username_equivalent = Recruiter.objects.filter(user__username=data["user"]["username"])
            if username_equivalent.exists() and username_equivalent[0].user.id != instance.user.id:
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = {}
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        else:
            return JsonResponse(serialiser.errors, status=400)

@csrf_exempt
def submissionListStudent(request):
    if request.method == "GET":
        submissions = Submission.objects.filter(student__user = request.user).select_related("student", "job", "line_manager")
        submissions_serialiser = DBAdminSubmissionStudentSerialiser(submissions, many=True)
        return JsonResponse(submissions_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        if data["_action"] == "create":
            serialiser = DBAdminSubmissionSerialiser(data=data)
            # if Student.objects.filter(user__id=request.user.id).exists():
            #     print("This student exists")
            # else:
            #     print("This student does not exist")
            if Student.objects.filter(user__id=request.user.id).exists():
                data["date_submitted"] = datetime.datetime.now().strftime("%Y-%m-%d")
                if serialiser.is_valid():
                    student = Student.objects.get(user__id=request.user.id)
                    if student.hours_worked + int(data.get("hours")) <= 15:
                        serialiser.create(validated_data=data)
                        student.hours_worked += int(data.get("hours"))
                        student.save()
                        print(serialiser.data)
                        return JsonResponse(serialiser.data, status=201)
                    else:
                        return JsonResponse({"message": "This goes over the hours allowed"}, status=403)
                else:
                    print(serialiser.errors)
                    return JsonResponse({"message": "Invalid field(s) but idk which one(s), well there's only four so you figure it out", "errors": serialiser.errors}, status=400)
            else:
                return JsonResponse({"message": "Authentication failed"}, status=403)
        elif data["_action"] == "update":
            instance = Submission.objects.get(id=data["_id"])
            data["accepted"] = instance.accepted
            print(data)
            serialiser = DBAdminSubmissionSerialiser(data=data)
            if serialiser.is_valid(raise_exception=ValueError):
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)

# @csrf_exempt
# def submissionListRecruiter(request):
#     if request.method == "GET":
#         submissions = RecruiterSubmission.objects.filter(recruiter_id__user__id=request.user.id).select_related("recruiter")
#         print(submissions)
#         submissions_serialiser = RecruiterSubmissionSerialiser(submissions, many=True)
#         return JsonResponse(submissions_serialiser.data, safe=False)
# 
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         if data["_action"] == "update":
#             instance = RecruiterSubmission.objects.get(id=data["_id"])
#             data["accepted"] = instance.accepted
#             print(data)
#             serialiser = RecruiterSubmissionSerialiser(data=data)
#             if serialiser.is_valid(raise_exception=ValueError):
#                 serialiser.update(instance=instance, validated_data=data)
#                 return JsonResponse(serialiser.data, status=201)
#             else:
#                 return JsonResponse(serialiser.errors, status=400)

@csrf_exempt
def jobList(request):
    if request.method == "GET":
        if request.user.user_type == "Recruiter":
            jobs = Job.objects.filter(recruiter__user=request.user)
        else:
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
        else:
            if request.user.user_type == "Recruiter":
                data["recruiter"] = Recruiter.objects.get(user=request.user).id
            if serialiser.is_valid():
                if data["_action"] == "create":
                    serialiser.create(validated_data=data)
                elif data["_action"] == "update":
                    instance = Job.objects.get(id=data["_id"])
                    serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)

@api_view(["GET"])
def jobDetail(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == "GET":
        job_serialiser = DBAdminJobDetailSerialiser(job);
        return Response(job_serialiser.data)
    # ad POST l8r

@csrf_exempt
def lineManagerList(request):
    if request.method == "GET":
        linemanagers = LineManager.objects.all()
        linemanagers_serialiser = DBAdminLineManagerSerialiser(linemanagers, many=True)
        return JsonResponse(linemanagers_serialiser.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = DBAdminLineManagerSerialiser(data=data)
        if data["_action"] == "deleteMultiple":
            for entry_id in data["to_delete"]:
                instance = LineManager.objects.get(id=entry_id)
                instance.user.delete()
                instance.delete()
            return JsonResponse(data={"message": "Deleted stuff"}, status=200)
        elif data["_action"] == "create":
            username_equivalent = LineManager.objects.filter(user__username=data["user"]["username"])
            if username_equivalent.exists():
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = {}
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.create(validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "update":
            instance = LineManager.objects.get(id=data["_id"])
            if "password" not in data["user"] or data["user"]["password"] == "":
                data["user"]["password"] = instance.user.password
            username_equivalent = CampusUser.objects.filter(username=data["user"]["username"])
            if (username_equivalent.exists() and username_equivalent[0].id != instance.user.id):
                serialiser.is_valid()
                return_data = serialiser.errors
                if "user" not in return_data:
                    return_data["user"] = None
                if "username" not in return_data["user"]:
                    return_data["user"]["username"] = [duplicate_username_message]
                else:
                    return_data["user"]["username"].append(duplicate_username_message)
                return JsonResponse(return_data, status=400)
            elif serialiser.is_valid():
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        else:
            return JsonResponse(serialiser.errors, status=400)

@api_view(["GET"])
def lineManagerDetail(request, pk):
    line_manager = LineManager.objects.get(id=pk)
    if request.method == "GET":
        linemanager_serialiser = DBAdminLineManagerDetailSerialiser(line_manager)
        return Response(linemanager_serialiser.data)

@api_view(["GET"])
def getLineManagersFromJob(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == "GET":
        linemanagers = LineManager.objects.filter(recruiter=job.recruiter)
        linemanagers_json = DBAdminLineManagerSerialiser(linemanagers, many=True)
        return JsonResponse(linemanagers_json.data, safe=False)

@api_view(["GET"])
def recruiterDetail(request, pk):
    recruiter = Recruiter.objects.get(id=pk)
    if request.method == "GET":
        recruiter_serialiser = DBAdminRecruiterDetailSerialiser(recruiter)
        return Response(recruiter_serialiser.data)

@csrf_exempt
def currentUser(request):
    if request.method == "GET":
        users = [request.user]
        users_serialiser = UserSerialiser(users, many=True)
        return JsonResponse(users_serialiser.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serialiser = UserSerialiser(data=data)
        if data["_action"] == "create":
            if serialiser.is_valid():
                serialiser.create(validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "update":
            # instance = Student.objects.get(user=User.objects.get(id=data["_id"]))
            instance = CampusUser.objects.get(id=data["_id"])
            if "password" not in data or data["password"] == "":
                data["password"] = instance.password
            if serialiser.is_valid():
                serialiser.update(instance=instance, validated_data=data)
                return JsonResponse(serialiser.data, status=201)
            else:
                return JsonResponse(serialiser.errors, status=400)
        elif data["_action"] == "delete":
            serialiser.delete(instance=CampusUser.objects.get(id=data["_id"]))
            return JsonResponse(data={"message": "Deleted your profile"}, status=200)
        else:
            print("action not found")

class HttpResponseInternalServerError(JsonResponse):
  def __init__(self, message):
    super().__init__({'message' : message}, status=503)
