from rest_framework import serializers
from master.models import Student, Submission, Job, LineManager
from django.contrib.auth.models import User

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class DBAdminStudentSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Student
        fields = ('user', 'on_visa')
    
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerialiser.create(UserSerialiser(), validated_data=user_data)
        student, created = Student.objects.update_or_create(user=user, on_visa=validated_data.pop("on_visa"))
        return student

class DBAdminJobSerialiser(serializers.ModelSerializer):
    student = DBAdminStudentSerialiser(many=True)
    # student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = Job
        fields = ['job_name', 'cost_code', 'pay_rate', 'student']

class DBAdminLineManagerSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    student = DBAdminStudentSerialiser(many=True, required=True)
    class Meta:
        model = LineManager
        fields = ['user', 'student']

class DBAdminSubmissionSerialiser(serializers.ModelSerializer):
    student = DBAdminStudentSerialiser(required=True)
    job = DBAdminJobSerialiser(required=True)
    line_manager = DBAdminLineManagerSerialiser(required=True)
    class Meta:
        model = Submission
        fields = ['student', 'job', 'line_manager', 'hours', 'date_worked', 'date_submitted', 'accepted']

