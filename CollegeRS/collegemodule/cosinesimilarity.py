import pandas as pd
from django import db
from django_pandas.io import read_frame

from .models import PreferenceCategory, User, CollegeEntityMaster, CollegeAffiliationsPreference, Profile


def findsimilarpreferencefunc(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    preferences = profile.preferences.all()
    profile_preference_df = read_frame(preferences)
    print(profile_preference_df)

    colleges = CollegeAffiliationsPreference.objects.all()
    college_df = read_frame(colleges)
    college_df['preferenceId'] = college_df['preferenceId'].apply(lambda x : x.split(".")[0])
    college_df['preferenceId'] = college_df['preferenceId'].astype('int64')

    user_pref_similar_colz = profile_preference_df.merge(college_df, left_on="id", right_on="preferenceId")
    user_pref_similar_colz.drop(["id_x", "id_y"], inplace=True, axis=1)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    user_pref_similar_colz['college_program'] = user_pref_similar_colz['collegeId'] + ", " + \
                                                user_pref_similar_colz['affiliationId']

    user_pref_similar_colz['preferences'] = user_pref_similar_colz['categoryName'] + " - " + \
                                            user_pref_similar_colz['subCategory'] + " - " + \
                                            user_pref_similar_colz['value']

    user_pref_similar_colz = user_pref_similar_colz[['preferences', 'college_program']]
    # print( user_pref_similar_colz)
    # print(user_pref_similar_colz.pivot_table(index=['college_program'], values=['preferences'], aggfunc='count'))
    # print(user_pref_similar_colz.groupby('college_program').size().unstack(fill_value=0))
    final_df = user_pref_similar_colz.groupby(['preferences', 'college_program']).size().unstack(
        fill_value=0.0)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # final_df['Best_College'] = [1.0, 0.9, 0.5, 0.5, 0.7]
    # final_df['Best_College'] = pd.Series(data=pd.np.random.uniform(0.589898, 0.008879), index=final_df.index)
    final_df['Best_College'] = pd.Series(data=pd.np.random.uniform(0.789898, 0.887989), index=final_df.index)
    recommended_df = final_df['Best College, Master of Computer Application(MCA) , Purbanchal University']
    # recommended_df = pd.DataFrame(data=float(1.0), index=final_df.index)

    # recommended_df = final_df['Best_College']
    print(recommended_df)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(final_df)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    colz_courses_likedatata = final_df.corrwith(recommended_df)
    final_user_recommendation = pd.DataFrame(colz_courses_likedatata, columns=['Correlation'])
    print(final_user_recommendation.head())
    final_user_recommendation.fillna(0.0, inplace=True)
    final_user_recommendation_sorted = final_user_recommendation.sort_values("Correlation", ascending=False)
    final_user_recommendation_sorted.drop("Best_College", axis=0, inplace=True)
    final_user_recommendation_sorted.drop("Best College, Master of Computer Application(MCA) , Purbanchal University", axis=0, inplace=True)
    return list(final_user_recommendation_sorted.head(5).index)




