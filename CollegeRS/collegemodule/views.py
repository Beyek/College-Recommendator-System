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
        # profile = Profile.objects.get(user=user)
        # preferences = profile.preferences.all()
        # profile_preference_df = read_frame(preferences)
        # print(profile_preference_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # # profile_df = read_frame(profile)
        # # print(profile_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # preference = PreferenceCategory.objects.all()
        # preferences_df = read_frame(preference)
        # print(preferences_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # colleges = CollegeAffiliationsPreference.objects.all()
        # print(CollegeAffiliationsPreference.objects.all())
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # college_df = read_frame(colleges)
        # print(college_df)
        # profile_preference_college_df = profile_preference_df.merge(college_df, left_on="id", right_on="preferenceId")
        # print(profile_preference_college_df)

        profile = Profile.objects.get(user=user)
        preferences = profile.preferences.all()
        profile_preference_df = read_frame(preferences)
        print(profile_preference_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # # profile_df = read_frame(profile)
        # # print(profile_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # preference = PreferenceCategory.objects.all()
        # preferences_df = read_frame(preference)
        # print(preferences_df)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        colleges = CollegeAffiliationsPreference.objects.all()

        # print(CollegeAffiliationsPreference.objects.all())
        preference_cate = PreferenceCategory.objects.all()
        df_pre = read_frame(preference_cate)
        # print(df_pre)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        college_df = read_frame(colleges)
        college_df['preferenceId'] = college_df['preferenceId'].apply(lambda x: x.split(".")[0])
        college_df['preferenceId'] = college_df['preferenceId'].astype('int64')
        # print(college_df)
        profile_preference_college_df = profile_preference_df.merge(college_df, left_on="id", right_on="preferenceId")
        # print(profile_preference_college_df)
        profile_preference_college_df.drop(["id_x", "id_y"], inplace=True, axis=1)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(profile_preference_college_df.pivot_table(columns='collegeId', index=""))
        profile_preference_college_df['college_program'] = profile_preference_college_df['collegeId'] + ", "+ \
                                                           profile_preference_college_df['affiliationId']

        profile_preference_college_df['preferences'] = profile_preference_college_df['categoryName'] + " - " + \
                                                       profile_preference_college_df['subCategory'] + " - " + \
                                                       profile_preference_college_df['value']

        profile_preference_college_df = profile_preference_college_df[['preferences', 'college_program']]
        # print( profile_preference_college_df)
        # print(profile_preference_college_df.pivot_table(index=['college_program'], values=['preferences'], aggfunc='count'))
        # print(profile_preference_college_df.groupby('college_program').size().unstack(fill_value=0))
        final_df = profile_preference_college_df.groupby(['preferences', 'college_program']).size().unstack(fill_value=0.0)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>")
        final_df['Best College'] = [1.0,0.0,0.4,0.0,0.9]
        # recomemded_df = pd.DataFrame(columns=["Best College"],data=np.random.randint(3,5), index=final_df.index)
        # recomemded_df = pd.DataFrame(columns=["Best College"], data=[1.0,0.3,0.4,0.7,0.9], index=final_df.index)
        recomemded_df = final_df['Best College']
        print(recomemded_df)

        print(recomemded_df)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>")
        print(final_df)

        # for col in final_df.columns:
        #

        print(recomemded_df)
        movies_like_forest_gump = final_df.corrwith(recomemded_df)
        corr_forrest_gump = pd.DataFrame(movies_like_forest_gump, columns=['Correlation'])
        # corr_forrest_gump.dropna(inplace=True)
        print(corr_forrest_gump.head())
        corr_forrest_gump.fillna(0, inplace=True)
        corr_forrest_gump_sorted = corr_forrest_gump.sort_values("Correlation", ascending=False)
        corr_forrest_gump_sorted.drop("Best College", axis=0, inplace=True)
        colleges = list(corr_forrest_gump_sorted.head(5).index)
        # print(movies_like_forest_gump.head())
        # return render(request, "",context={"Colleges": colleges})
        # print(profile_preference_college_df)

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
