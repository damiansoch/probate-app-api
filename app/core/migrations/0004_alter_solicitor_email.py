# Generated by Django 3.2.25 on 2024-06-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240607_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitor',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
