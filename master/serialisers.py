from rest_framework import serializers
from master.models import Student, Submission, Job, LineManager

class DBAdminStudentSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'on_visa']

class DBAdminSubmissionSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(source='student.user.username', read_only=True)
    first_name = serializers.CharField(source='student.user.first_name', read_only=True)
    last_name = serializers.CharField(source='student.user.last_name', read_only=True)
    job_name = serializers.CharField(source='job.job_name', read_only=True)
    line_manager_username = serializers.CharField(source='line_manager.user.username', read_only=True)
    class Meta:
        model = Submission
        fields = ['username', 'first_name', 'last_name', 'job_name', 'line_manager_username', 'hours', 'date_worked', 'date_submitted', 'accepted']

class DBAdminJobSerialiser(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = Job
        fields = ['job_name', 'cost_code', 'pay_rate', 'student_username']

class DBAdminLineManagerSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = LineManager
        fields = ['username', 'first_name', 'last_name', 'student_username']
