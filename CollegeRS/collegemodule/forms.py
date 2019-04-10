from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, PreferenceCategory

from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    name = forms.CharField(max_length=100)
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    email_address = forms.CharField(max_length=100)
    preferences = forms.ModelMultipleChoiceField(queryset=PreferenceCategory.objects.all())

    class Meta:
        model = User
        fields = ('username', 'name', 'sex', 'email_address', 'preferences', 'password1', 'password2', )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Profile
        fields = ('user', 'email_address', 'name', 'description', 'sex', 'preferences')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('user', 'email_address', 'name', 'description', 'sex', 'preferences')