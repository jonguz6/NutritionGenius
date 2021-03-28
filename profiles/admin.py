from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from profiles.forms import ProfileForm
from profiles.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = "Profile"
    can_delete = False
    form = ProfileForm


class MyUserAdmin(UserAdmin):    
    inlines = [
        ProfileInline,
    ]


admin.site.register(Profile)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
