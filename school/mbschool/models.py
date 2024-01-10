from datetime import date

from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=20, unique=True)
    course_status = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    student_name = models.CharField(max_length=30, null=False)
    student_email = models.EmailField(unique=True, null=False)
    enrolled_year = models.DateField(default=date.today)
    student_status = models.BooleanField(default=True)
    # courses = models.ManyToManyField(Course, related_name='student_courses')

    def __str__(self):
        return self.student_name


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=30, null=False)
    teacher_email = models.EmailField(unique=True, null=False)
    teacher_status = models.BooleanField(default=True)

    def __str__(self):
        return self.teacher_name


