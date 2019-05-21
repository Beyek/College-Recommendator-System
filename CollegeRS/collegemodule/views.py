import logging, sys

from django.contrib.auth.models import User
import pandas as pd
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django_pandas.io import read_frame

from collegemodule.cosinesimilarity import findsimilarpreferencefunc
from collegemodule.forms import SignUpForm
from .models import CollegeEntityMaster, PreferenceCategory, CollegeAffiliationsPreference, Profile
import numpy as np

# Get an instance of a logger
logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.email_address = form.cleaned_data.get('email_address')
            user.profile.name = form.cleaned_data.get('name')
            user.profile.sex = form.cleaned_data.get('sex')
            user.profile.preferences.set(form.cleaned_data.get('preferences'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('college_detail')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    colleges = CollegeEntityMaster.objects.all()
    return render(request, 'home.html', {'colleges': colleges})

# def college_detail(request, collegeId):
#     try:
#         college = CollegeEntityMaster.objects.get(id=collegeId)
#     except CollegeEntityMaster.DoesNotExist:
#         raise Http404('College not found')
#     return render(request, 'college_details.html', {'college': college})


def college_detail(request):
    try:

        colleges_list = findsimilarpreferencefunc(request)
        size = len(colleges_list)
        # print(colz_courses_likedatata.head())
        # return render(request, "",context={"Colleges": colleges})
        # print(user_pref_similar_colz)

        # profilePreferences = Profile.preferences
        # data = pd.merge(preferences_df, college_df, on='id')
        # print(data)

        # college_data = pd.merge(college_df, preferences_df, on='preferenceId')
        # print(college_data.head())
        # return df.head()
        # for preference in preferences.to_dataframe():
        #     print("preference -------------> "+preference)

    except CollegeEntityMaster.DoesNotExist:
        raise Http404('College not found')
    return render(request, 'college_details.html', context={"colleges": colleges_list, "size": size})
