from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from master.models import CampusUser

admin.site.register(CampusUser, UserAdmin)
