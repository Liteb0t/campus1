# Generated by Django 5.1.6 on 2025-04-11 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_job_recruiter_submission_archived_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linemanager',
            name='student',
        ),
        migrations.AddField(
            model_name='linemanager',
            name='recruiter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='master.recruiter'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='date_submitted',
            field=models.DateField(default='2025-04-11'),
        ),
    ]
