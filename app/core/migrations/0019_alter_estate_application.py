# Generated by Django 3.2.25 on 2024-06-12 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_rename_expenses_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.application'),
        ),
    ]