from django.contrib import admin

from .models import CollegeEntityMaster, PreferenceCategory, Affiliations, CourseMaster, University, UserInfo


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


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_address',  'sex']
