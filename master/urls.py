from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.userProfile, name="user_profile"),
    path("admin/", admin.site.urls),
    path("deleted_account", views.deletedAccount, name="deleted_account"),
    path("", views.homepage, name="homepage"),
    path("make_submission", views.makesubmissionpage, name="make_submission"),
    path("recruiter_profile", views.recruiterProfile, name="recruiter_profile"),
    path("access_data_browser", views.accessDataBrowser, name="access_data_browser"),
    path("access_student_submission", views.accessStudentSubmission, name="access_student_submission"),
    path("access_recruiter_submission", views.accessRecruiterSubmission, name="access_recruiter_submission"),
    path("access_manager_approval", views.accessRecruiterSubmission, name="access_manager_approval"),
    path("api/users/", views.currentUser, name="userList"),
    path("api/students/", views.studentList, name="studentList"),
    path("api/student/<int:pk>", views.studentDetail, name="studentDetail"),
    path("api/submissions/", views.submissionList, name="submissionList"),
    path("api/submission/<int:pk>", views.submissionDetail, name="submissionDetail"),
    path("api/recruiters/", views.recruiterList, name="recruiterList"),
    path("api/recruiter/<int:pk>", views.recruiterDetail, name="recruiterDetail"),
    path("api/jobs/", views.jobList, name="jobList"),
    path("api/job/<int:pk>", views.jobDetail, name="jobDetail"),
    path("api/lineManagers/", views.lineManagerList, name="lineManagerList"),
    path("api/lineManagersFromJob/<int:pk>", views.getLineManagersFromJob, name="getLineManagersFromJob"),
    path("api/lineManager/<int:pk>", views.lineManagerDetail, name="lineManagerDetail"),
    path("api/submissionsStudent/", views.submissionListStudent, name="submissionListStudent"),
    # path("api/submissionsRecruiter/", views.submissionListRecruiter, name="submissionListRecruiter"),
]
