from master.models import Student

def resetStudentHours():
    for student in Student.objects.all():
        student.hours_worked = 0
        student.save()
