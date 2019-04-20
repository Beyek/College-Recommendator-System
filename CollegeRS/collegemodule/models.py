from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
    email_address = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    preferences = models.ManyToManyField('PreferenceCategory', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PreferenceCategory(models.Model):
    categoryName = models.CharField(max_length=50)
    subCategory = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        unique_together = ('categoryName', 'subCategory', 'value',)

    def __str__(self):
        return '%i. %s, %s' % (self.id, self.categoryName, self.value)


class CollegeEntityMaster(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    url = models.URLField()
    description = models.TextField(blank=True)
    affiliation = models.ManyToManyField('Affiliations', blank=True)

    def __str__(self):
        return self.name


class CollegeAffiliationsPreference(models.Model):
    collegeId = models.ForeignKey('CollegeEntityMaster', blank=False, on_delete=models.CASCADE)
    affiliationId = models.ForeignKey('Affiliations', blank=False, on_delete=models.CASCADE)
    preferenceId = models.ForeignKey('PreferenceCategory', blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('collegeId', 'affiliationId', 'preferenceId',)


class Affiliations(models.Model):
    university = models.ForeignKey('University', null=False, blank=False, on_delete=models.CASCADE)
    degree = models.ForeignKey('CourseMaster', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('university', 'degree',)

    def __str__(self):
        return '%s %s %s' % (self.degree, ",", self.university)


class University(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CourseMaster(models.Model):
    degree = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.degree
