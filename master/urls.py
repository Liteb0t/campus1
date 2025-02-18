from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/logged_out", views.logged_out, name="logged_out"),
    path("", views.index, name="index"),
    path("homepage", views.homepage, name="homepage"),
    path("secure", views.secure, name="secure"),
    path("profile", views.profile, name="profile"),
 path("access_db_admin", views.access_db_admin, name="access_db_admin"),
]