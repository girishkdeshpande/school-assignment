from django.db import models


class Student(models.Model):
    student_name = models.CharField(max_length=30)
    student_email = models.EmailField(unique=True)
    enrolled_year = models.DateField('admission date')
    student_status = models.BooleanField(default=True)

    def __str__(self):
        return self.student_name


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=30)
    teacher_email = models.EmailField(unique=True)
    teacher_status = models.BooleanField(default=True)

    def __str__(self):
        return self.teacher_name


class Course(models.Model):
    course_name = models.CharField(max_length=20, unique=True)
    course_status = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name
