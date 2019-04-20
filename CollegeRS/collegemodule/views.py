import logging, sys

from django.contrib.auth.models import User
import pandas as pd
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django_pandas.io import read_frame
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
            return redirect('home')
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
        user = request.user
        profile = Profile.objects.get(user=user)
        preferences = profile.preferences.all()
        profile_preference_df = read_frame(preferences)
        print(profile_preference_df)

        colleges = CollegeAffiliationsPreference.objects.all()
        college_df = read_frame(colleges)
        college_df['preferenceId'] = college_df['preferenceId'].apply(lambda x: x.split(".")[0])
        college_df['preferenceId'] = college_df['preferenceId'].astype('int64')

        user_pref_similar_colz = profile_preference_df.merge(college_df, left_on="id", right_on="preferenceId")
        user_pref_similar_colz.drop(["id_x", "id_y"], inplace=True, axis=1)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        user_pref_similar_colz['college_program'] = user_pref_similar_colz['collegeId'] + ", "+ \
                                                    user_pref_similar_colz['affiliationId']

        user_pref_similar_colz['preferences'] = user_pref_similar_colz['categoryName'] + " - " + \
                                                user_pref_similar_colz['subCategory'] + " - " + \
                                                user_pref_similar_colz['value']

        user_pref_similar_colz = user_pref_similar_colz[['preferences', 'college_program']]
        # print( user_pref_similar_colz)
        # print(user_pref_similar_colz.pivot_table(index=['college_program'], values=['preferences'], aggfunc='count'))
        # print(user_pref_similar_colz.groupby('college_program').size().unstack(fill_value=0))
        final_df = user_pref_similar_colz.groupby(['preferences', 'college_program']).size().unstack(fill_value=0.0000000000000)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        final_df['Best_College'] = [1.0, 0.9, 0.5, 0.5, 0.7]
        # final_df['Best_College'] = pd.Series(data=np.random.uniform(0.5, 1.0), index=final_df.index)
        recommended_df = final_df['Best_College']
        # recommended_df = pd.DataFrame(data=float(1.0), index=final_df.index)

        # recommended_df = final_df['Best_College']
        print(recommended_df)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(final_df)

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        colz_courses_likedatata = final_df.corrwith(recommended_df)
        corr_forrest_gump = pd.DataFrame(colz_courses_likedatata, columns=['Correlation'])
        print(corr_forrest_gump.head())
        corr_forrest_gump.fillna(0.0, inplace=True)
        corr_forrest_gump_sorted = corr_forrest_gump.sort_values("Correlation", ascending=False)
        corr_forrest_gump_sorted.drop("Best_College", axis=0, inplace=True)
        colleges = list(corr_forrest_gump_sorted.head(5).index)
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
    return render(request, 'college_details.html', context={"colleges": colleges})
