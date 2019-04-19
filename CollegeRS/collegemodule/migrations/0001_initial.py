# Generated by Django 2.1.7 on 2019-04-16 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeAffiliationsPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegemodule.Affiliations')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeEntityMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact_no', models.CharField(max_length=10)),
                ('url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('affiliation', models.ManyToManyField(blank=True, to='collegemodule.Affiliations')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreferenceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=50, unique=True)),
                ('subCategory', models.CharField(blank=True, max_length=50, null=True)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('email_address', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('preferences', models.ManyToManyField(blank=True, to='collegemodule.PreferenceCategory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='preferencecategory',
            unique_together={('categoryName', 'value')},
        ),
        migrations.AddField(
            model_name='collegeaffiliationspreference',
            name='collegeId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegemodule.CollegeEntityMaster'),
        ),
        migrations.AddField(
            model_name='collegeaffiliationspreference',
            name='preferenceId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegemodule.PreferenceCategory'),
        ),
        migrations.AddField(
            model_name='affiliations',
            name='degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegemodule.CourseMaster'),
        ),
        migrations.AddField(
            model_name='affiliations',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegemodule.University'),
        ),
        migrations.AlterUniqueTogether(
            name='collegeaffiliationspreference',
            unique_together={('collegeId', 'affiliationId', 'preferenceId')},
        ),
        migrations.AlterUniqueTogether(
            name='affiliations',
            unique_together={('university', 'degree')},
        ),
    ]
