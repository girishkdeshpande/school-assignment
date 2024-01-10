from rest_framework import serializers
from .models import Student, Course, Teacher


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_status']


class StudentSerializer(serializers.ModelSerializer):
    # courses = CourseSerializer(many=True)

    class Meta:
        model = Student
        fields = ['id', 'student_name', 'student_email', 'enrolled_year', 'student_status']


class StudentPost(StudentSerializer):
    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'enrolled_year']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_name', 'teacher_email', 'teacher_status']
