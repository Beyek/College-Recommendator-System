from django import db
from.models import PreferenceCategory, User, CollegeEntityMaster, CollegeAffiliationsPreference


def findsimilarpreferencefunc(userId):
    print("Logging message", flush=True)
    profile = User.objects.get(userId).profile
    preference = profile.preferences.all()
    preference_df = preference.to_dataframe()
    return preference_df.head()




