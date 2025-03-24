from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from master.models import Student, Submission, Job, LineManager
from django.contrib.auth.models import User

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class DBAdminStudentSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'user', 'on_visa')

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerialiser.create(UserSerialiser(), validated_data=user_data)
        student = Student.objects.create(user=user, on_visa=validated_data.pop("on_visa"))
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.user.username = user_data["username"]
        instance.user.first_name = user_data["first_name"]
        instance.user.last_name = user_data["last_name"]
        # instance.user.last_name = validated_data.get("last_name")
        instance.on_visa = validated_data["on_visa"]
        instance.user.save()
        instance.save()
        return instance

    def delete(self, instance):
        instance.user.delete()
        instance.delete()
        return instance

class DBAdminJobSerialiser(serializers.ModelSerializer):
    student = DBAdminStudentSerialiser(many=True)
    # student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = Job
        fields = ['job_name', 'cost_code', 'pay_rate', 'student']

    def create(self, validated_data):
        job = Job.objects.create(job_name=validated_data.pop("job_name"), cost_code=validated_data.pop("cost_code"), pay_rate=validated_data.pop("pay_rate"), student=None)
        return job

    def update(self, instance, validated_data):
        instance.student = validated_data["student"]
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance

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

    def create(self, validated_data):
        submission = Submission.objects.create(student=student, job=job, line_manager=line_manager, hours=validated_data.pop("hours"), date_worked=validated_data.pop("date_worked"), date_submitted=validated_data.pop("date_submitted"), accepted=validated_data.pop("accepted"))
        return submission

    def update(self, instance, validated_data):
        #student_data = validated_data.pop("student")
        #job_data = validated_data.pop("job")
        #manager_data = validated_data.pop("line_manager")

        #instance.student = validated_data["student"]
        #instance.job = validated_data["job"]
        #instance.line_manager = validated_data["line_manager"]
        #instance.hours = validated_data["hours"]
        #instance.date_worked = validated_data["date_worked"]
        #instance.date_submitted = validated_data["date_submitted"]
        instance.accepted = validated_data["accepted"]
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance