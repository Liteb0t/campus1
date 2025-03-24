from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepage, name="homepage"),
    path("profile", views.profile, name="profile"),
    path("MakeSubmission", views.makesubmissionpage, name="makesubmission"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("admin_profile", views.admin_profile, name="admin_profile"),
    path("access_db_admin", views.access_db_admin, name="access_db_admin"),
    path("api/students/", views.studentList, name="studentList"),
    path("api/submissions/", views.submissionList, name="submissionList"),
    path("api/jobs/", views.jobList, name="jobList"),
    path("api/lineManagers/", views.lineManagerList, name="lineManagerList"),
]
