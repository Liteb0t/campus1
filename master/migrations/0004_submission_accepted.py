# Generated by Django 5.1.6 on 2025-02-20 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='accepted',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
