from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "templatetest.html")

def templatetest(request):
    return render(request, "templatetest.html")

def logged_out(request):
    return render(request, "registration/logged_out.html")

@login_required
def secure(request):
    return render(request, "secure.html")