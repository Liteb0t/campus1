from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/logged_out", views.logged_out, name="logged_out"),
    path("", views.index, name="index"),
    path("templatetest", views.templatetest, name="templatetest"),
    path("secure", views.secure, name="secure"),
    path("access_db_admin", views.access_db_admin, name="access_db_admin"),
    path("data", views.data, name='data'),
    ]