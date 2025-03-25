from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("deleted_account", views.deleted_account, name="deleted_account"),
    path("", views.homepage, name="homepage"),
    path("profile", views.profile, name="profile"),
    path("MakeSubmission", views.makesubmissionpage, name="makesubmission"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("access_db_admin", views.access_db_admin, name="access_db_admin"),
    path("access_student_submission", views.access_student_submission, name="access_student_submission"),
    path("api/students/", views.studentList, name="studentList"),
    path("api/users/", views.currentUser, name="userList"),
    path("api/submissions/", views.submissionList, name="submissionList"),
    path("api/submissionsStudent/", views.submissionListStudent, name="submissionListStudent"),
    path("api/jobs/", views.jobList, name="jobList"),
    path("api/job/<int:pk>", views.jobDetail, name="jobDetail"),
    path("api/lineManagers/", views.lineManagerList, name="lineManagerList"),
]
