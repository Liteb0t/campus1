# Generated by Django 5.1.6 on 2025-03-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_remove_recruiter_email_remove_recruiter_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter_submission',
            name='accepted',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='accepted',
            field=models.BooleanField(null=True),
        ),
    ]
