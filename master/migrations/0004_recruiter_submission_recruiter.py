# Generated by Django 5.1.7 on 2025-03-25 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_alter_recruiter_submission_accepted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter_submission',
            name='recruiter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='master.recruiter'),
            preserve_default=False,
        ),
    ]
