# Generated by Django 3.2.25 on 2024-06-07 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_applicationstatusid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApplicationStatusId',
            new_name='ApplicationStatus',
        ),
    ]
