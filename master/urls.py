from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepage, name="homepage"),
    path("profile", views.profile, name="profile"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("admin_profile", views.admin_profile, name="admin_profile"),
    path("access_db_admin", views.access_db_admin, name="access_db_admin"),
    path("access_db_admin_old", views.access_db_admin_old, name="adminSHU"),
    path("access_db_student", views.access_db_student, name="student"),
    path("UpdateStudent/<int:id>", views.updatestudent, name="update"),
    path("DeleteStu/<int:id>", views.deletestudent, name="delete"),
    path("DeleteSub/<int:id>", views.deletesubmission, name="deletesub"),
    path("DeleteJob/<int:id>", views.deletejob, name="deletejob"),
    path("api/students/", views.studentList, name="studentList"),
    path("api/submissions/", views.submissionList, name="submissionList"),
    path("api/jobs/", views.jobList, name="jobList"),
    path("api/lineManagers/", views.lineManagerList, name="lineManagerList"),
]
