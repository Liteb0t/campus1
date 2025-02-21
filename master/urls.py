from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepage, name="homepage"),
    path("secure", views.secure, name="secure"),
    path("profile", views.profile, name="profile"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("admin_profile", views.admin_profile, name="admin_profile"),
    path("access_db_admin", views.access_db_admin, name="adminSHU"),
    path("access_db_student", views.access_db_student, name="student"),
    path("UpdateStudent/<int:id>", views.updatestudent, name="update"),
    path("DeleteStu/<int:id>", views.deletestudent, name="delete"),
    path("DeleteSub/<int:id>", views.deletesubmission, name="deletesub"),
    path("DeleteJob/<int:id>", views.deletejob, name="deletejob"),

]