# Generated by Django 3.2.25 on 2024-06-11 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20240611_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='dispute',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='description',
            field=models.TextField(),
        ),
    ]