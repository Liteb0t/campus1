from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepage, name="homepage"),
    path("secure", views.secure, name="secure"),
    path("profile", views.profile, name="profile"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("admin_profile", views.admin_profile, name="admin_profile"),
    path("admin", views.access_db_admin, name="access_db_admin"),
    path("student", views.access_db_student, name="access_db_student"),
    path("TempUpdatePageForTesting/<int:id>", views.updatestudent, name="update"),

]