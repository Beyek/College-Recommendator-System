from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import CollegeEntityMaster, PreferenceCategory, Affiliations, CourseMaster, University, Profile, \
    CollegeAffiliationsPreference


class EmployeeInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'userinfo'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(CollegeEntityMaster)
class CollegeEntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_no', 'url']


@admin.register(Affiliations)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ['university', 'degree']


@admin.register(University)
class UniversityEntityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CourseMaster)
class CourseEntityAdmin(admin.ModelAdmin):
    list_display = ['degree']


@admin.register(PreferenceCategory)
class PreferenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName', 'subCategory', 'value']


@admin.register(Profile)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_address',  'sex']


@admin.register(CollegeAffiliationsPreference)
class CollegeWithAffiliationAdmin(admin.ModelAdmin):
    list_display = ['collegeId', 'affiliationId',  'preferenceId']
