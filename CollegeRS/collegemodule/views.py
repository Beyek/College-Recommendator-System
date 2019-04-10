from django.http import Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from collegemodule.forms import SignUpForm
from.models import CollegeEntityMaster


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.email_address = form.cleaned_data.get('email_address')
            user.profile.name = form.cleaned_data.get('name')
            user.profile.sex = form.cleaned_data.get('sex')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    colleges = CollegeEntityMaster.objects.all()
    return render(request, 'home.html', {'colleges': colleges})


def college_detail(request, collegeId):
    try:
        college = CollegeEntityMaster.objects.get(id=collegeId)
    except CollegeEntityMaster.DoesNotExist:
        raise Http404('College not found')
    return render(request, 'college_details.html', {'college': college})
