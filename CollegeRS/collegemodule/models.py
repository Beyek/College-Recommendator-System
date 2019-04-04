from django.db import models


class UserInfo(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    email_address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    auth_token = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
    registered_date = models.DateTimeField()
    preferences = models.ManyToManyField('PreferenceCategory', blank=True)


class PreferenceCategory(models.Model):
    categoryName = models.CharField(max_length=50, unique=True)
    subCategory = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        unique_together = ('categoryName', 'value',)

    def __str__(self):
        return '%s (%s)' % (self.categoryName, self.value)


class CollegeEntityMaster(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    url = models.URLField()
    description = models.TextField(blank=True)
    affiliation = models.ManyToManyField('Affiliations', blank=True)

    def __str__(self):
        return self.name


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
