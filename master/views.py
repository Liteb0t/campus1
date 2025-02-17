from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from master.models import Job, Student, LineManager, Submission
from django.template import loader

def index(request):
    return HttpResponse("Hi guys this is the page that is not behind the security wall, go to /secure or something to test that")

def templatetest(request):
    return render(request, "templatetest.html")

def logged_out(request):
    return render(request, "registration/logged_out.html")

@login_required
def secure(request):
    return render(request, "secure.html")

def access_db_admin(request):
    Jobs = Job.objects.all()
    Students = Student.objects.all()
    Submissions = Submission.objects.all()
    LineManagers = LineManager.objects.all()
    return render(request, "DB_View/access_db_admin.html", {"Jobs": Jobs})

'''
def data(request):
    Jobs = Job.objects.all().values()
    template = loader.get_template("data.html")
    context = {
        'Jobs':Jobs,
        'range': range(Job.objects.all().__len__())
    }
    return HttpResponse(template.render(context, request))
'''
def data(request):
    Jobs = Job.objects.all()
    return render(request, 'data.html', {"Jobs": Jobs})