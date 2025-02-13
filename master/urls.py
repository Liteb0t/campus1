from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/logged_out", views.logged_out, name="logged_out"),
    path("", views.index, name="index"),
    path("templatetest", views.templatetest, name="templatetest"),
    path("secure", views.secure, name="secure")
]