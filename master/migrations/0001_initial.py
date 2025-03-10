# Generated by Django 5.1.7 on 2025-03-10 12:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('first_Name', models.CharField(max_length=255)),
                ('last_Name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_visa', models.BooleanField(default=False)),
                ('visa_expiry', models.DateField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter_Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('accepted', models.BooleanField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.student')),
            ],
        ),
        migrations.CreateModel(
            name='LineManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ManyToManyField(to='master.student')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=255)),
                ('cost_code', models.CharField(max_length=255)),
                ('pay_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('student', models.ManyToManyField(to='master.student')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('date_worked', models.DateField()),
                ('date_submitted', models.DateField()),
                ('accepted', models.BooleanField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.job')),
                ('line_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.linemanager')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.student')),
            ],
        ),
    ]
