from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from.models import CollegeEntityMaster


def home(request):
    colleges = CollegeEntityMaster.objects.all()
    return render(request, 'home.html', {'colleges': colleges})


def college_detail(request, collegeId):
    try:
        college = CollegeEntityMaster.objects.get(id=collegeId)
    except CollegeEntityMaster.DoesNotExist:
        raise Http404('College not found')
    return render(request, 'college_details.html', {'college': college})
