# Generated by Django 2.1.7 on 2019-04-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegemodule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferencecategory',
            name='categoryName',
            field=models.CharField(max_length=50),
        ),
    ]
