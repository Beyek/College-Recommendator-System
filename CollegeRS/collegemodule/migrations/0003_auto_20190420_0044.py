# Generated by Django 2.1.7 on 2019-04-20 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collegemodule', '0002_auto_20190419_1455'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='preferencecategory',
            unique_together={('categoryName', 'subCategory', 'value')},
        ),
    ]