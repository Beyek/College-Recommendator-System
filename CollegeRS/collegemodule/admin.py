from django.contrib import admin

from .models import CollegeEntityMaster
from .models import Affiliations
from .models import CourseMaster
from .models import University


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
