from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.validators import UnicodeUsernameValidator
from master.models import Student, Submission, Job, LineManager, Recruiter, CampusUser # , RecruiterSubmission

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CampusUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            # Overrides the check for username, because the built-in duplicate username checker was causing problems
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
    def create(self, validated_data):
        user = CampusUser.objects.create_user(username=validated_data["username"], first_name=validated_data["first_name"], last_name=validated_data["last_name"], email=validated_data["email"], password=validated_data["password"], user_type=validated_data["user_type"])
        Token.objects.create(user=user)
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        if validated_data["password"] != instance.password:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def delete(self, instance):
        # token_to_delete = Token.objects.get(user=instance)
        instance.delete()
        return instance

class DBAdminStudentSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'user', 'on_visa', 'hours_worked', 'eligible_to_work')

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_type"] = "Student"
        user = UserSerialiser.create(UserSerialiser(), validated_data=user_data)
        student = Student.objects.create(user=user, on_visa=validated_data.pop("on_visa"), hours_worked=validated_data.pop("hours_worked"), eligible_to_work=validated_data.pop("eligible_to_work"))
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.user.username = user_data["username"]
        instance.user.first_name = user_data["first_name"]
        instance.user.last_name = user_data["last_name"]
        instance.user.email = user_data["email"]
        if user_data["password"] != instance.user.password:
            instance.user.set_password(user_data["password"])
        # instance.user.last_name = validated_data.get("last_name")
        instance.on_visa = validated_data["on_visa"]
        instance.hours_worked = validated_data["hours_worked"]
        instance.eligible_to_work = validated_data["eligible_to_work"]
        instance.user.save()
        instance.save()
        return instance

    def delete(self, instance):
        instance.user.delete()
        instance.delete()
        return instance

# class DBAdminStudentDetailSerialiser(serializers.ModelSerializer):
#     student = DBAdminStudentSerialiser(many=True, required=True)
#     user = UserSerialiser(required=True)
#     # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
#     # student_username = serializers.CharField(source='student.user.username', read_only=True)
#     class Meta:
#         model = LineManager
#         fields = ['id', 'user']

## Dont delet because we might want this later
# class DynamicFieldsModelSerialiser(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
# 
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
# 
#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerialiser, self).__init__(*args, **kwargs)
# 
#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
# 
# class SimpleStudentSerialiser(serializers.ModelSerialiser):
#     class Meta:
#         model = Student
#         fields = '__all__'

class DBAdminJobSerialiser(serializers.ModelSerializer):
    # student = DBAdminStudentSerialiser(many=True, required=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    recruiter = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all(), many=False)
    # student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'job_name', 'recruiter', 'cost_code', 'pay_rate', 'student']

    def create(self, validated_data):
        recruiter = Recruiter.objects.get(id=validated_data["recruiter"])
        job = Job.objects.create(job_name=validated_data.pop("job_name"), recruiter=recruiter, cost_code=validated_data.pop("cost_code"), pay_rate=validated_data.pop("pay_rate"))
        for student_item in validated_data["student"]:
            job.student.add(student_item)
        return job

    def update(self, instance, validated_data):
        instance.recruiter = Recruiter.objects.get(id=validated_data["recruiter"])
        instance.job_name = validated_data["job_name"]
        instance.cost_code = validated_data["cost_code"]
        instance.pay_rate = validated_data["pay_rate"]
        instance.save()
        instance.student.set(validated_data["student"])
        return instance

    def delete(self, instance):
        instance.delete()
        return instance

class DBAdminJobDetailSerialiser(serializers.ModelSerializer):
    student = DBAdminStudentSerialiser(many=True, required=True)
    recruiter = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all(), many=False)
    # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    # student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'job_name', 'recruiter', 'cost_code', 'pay_rate', 'student']

    # def create(self, validated_data):
    #     job = Job.objects.create(job_name=validated_data.pop("job_name"), cost_code=validated_data.pop("cost_code"), pay_rate=validated_data.pop("pay_rate"), student=student)
    #     return job

class DBAdminLineManagerSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    # student = DBAdminLineManagerSerialiser(many=True, required=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    class Meta:
        model = LineManager
        fields = ['id', 'user', 'student']

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_type"] = "LineManager"
        user = UserSerialiser.create(UserSerialiser(), validated_data=user_data)
        # student = LineManager.objects.create(user=user)
        line_manager = LineManager.objects.create(user=user)
        line_manager.student.set(validated_data["student"])
        return line_manager

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.user.username = user_data["username"]
        instance.user.first_name = user_data["first_name"]
        instance.user.last_name = user_data["last_name"]
        instance.user.email = user_data["email"]
        if user_data["password"] != instance.user.password:
            instance.user.set_password(user_data["password"])
        instance.user.save()
        instance.save()
        instance.student.set(validated_data["student"])
        return instance

    def delete(self, instance):
        instance.user.delete()
        instance.delete()
        return instance

class DBAdminLineManagerDetailSerialiser(serializers.ModelSerializer):
    student = DBAdminStudentSerialiser(many=True, required=True)
    user = UserSerialiser(required=True)
    # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    # student_username = serializers.CharField(source='student.user.username', read_only=True)
    class Meta:
        model = LineManager
        fields = ['id', 'user', 'student']


class DBAdminSubmissionSerialiser(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=False)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), many=False)
    line_manager = serializers.PrimaryKeyRelatedField(queryset=LineManager.objects.all(), many=False)
    # student = DBAdminStudentSerialiser(required=True)
    # job = DBAdminJobSerialiser(required=True)
    # line_manager = DBAdminLineManagerSerialiser(required=True)
    class Meta:
        model = Submission
        fields = ['id', 'student', 'job', 'line_manager', 'hours', 'date_worked', 'date_submitted', 'accepted', 'reviewed', 'archived']

    def create(self, validated_data):
        student = Student.objects.get(id=validated_data["student"])
        job = Job.objects.get(id=validated_data["job"])
        line_manager = LineManager.objects.get(id=validated_data["line_manager"])
        submission = Submission.objects.create(student=student, job=job, line_manager=line_manager, hours=validated_data["hours"], date_worked=validated_data["date_worked"])
        return submission

    def update(self, instance, validated_data):
        # student_from_json = validated_data.pop("student")
        # student_object = Student.objects.get(id=student_from_json["id"])
        #student_data = validated_data.pop("student")
        #job_data = validated_data.pop("job")
        #manager_data = validated_data.pop("line_manager")

        instance.student = Student.objects.get(id=validated_data["student"])
        instance.job = Job.objects.get(id=validated_data["job"])
        instance.line_manager = LineManager.objects.get(id=validated_data["line_manager"])
        instance.hours = validated_data["hours"]
        instance.date_worked = validated_data["date_worked"]
        # instance.date_submitted = validated_data["date_submitted"]
        instance.accepted = validated_data["accepted"]
        instance.archived = validated_data["archived"]
        instance.reviewed = validated_data["reviewed"]
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance

# class DBAdminSubmissionDetailSerialiser(serializers.ModelSerializer):
#     student = DBAdminStudentSerialiser(many=True, required=True)
#     # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
#     # student_username = serializers.CharField(source='student.user.username', read_only=True)
#     class Meta:
#         model = Submission
#         fields = ['id', 'job_name', 'cost_code', 'pay_rate', 'student']

class DBAdminRecruiterSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    class Meta:
        model = Recruiter
        fields = ('id', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_type"] = "Recruiter"
        user = UserSerialiser.create(UserSerialiser(), validated_data=user_data)
        recruiter = Recruiter.objects.create(user=user)
        return recruiter

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.user.username = user_data["username"]
        instance.user.first_name = user_data["first_name"]
        instance.user.last_name = user_data["last_name"]
        instance.user.email = user_data["email"]
        if user_data["password"] != instance.user.password:
            instance.user.set_password(user_data["password"])
        instance.user.save()
        instance.save()
        return instance

    def delete(self, instance):
        instance.user.delete()
        instance.delete()
        return instance

class DBAdminRecruiterDetailSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(required=True)
    class Meta:
        model = LineManager
        fields = ['id', 'user']

# class RecruiterSubmissionSerialiser(serializers.ModelSerializer):
#     student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=False)
#     recruiter = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all(), many=False)
# 
#     class Meta:
#         model = RecruiterSubmission
#         fields = ['id', 'hours', 'student', 'accepted', 'recruiter']
# 
#     def create(self, validated_data):
#         student = Student.objects.get(id=validated_data["student"])
#         recruiter = Recruiter.objects.get(id=validated_data["recruiter"])
#         submission = Submission.objects.create(student=student, hours=validated_data.pop("hours"), accepted=validated_data.pop("accepted"), recruiter=recruiter)
#         return submission
# 
#     def update(self, instance, validated_data):
#         instance.recruiter_id = Recruiter.objects.get(id=validated_data["recruiter"])
#         instance.student = Student.objects.get(id=validated_data["student"])
#         instance.accepted = validated_data["accepted"]
#         instance.save()
#         return instance
# 
#     def delete(self, instance):
#         instance.delete()
#         return instance
