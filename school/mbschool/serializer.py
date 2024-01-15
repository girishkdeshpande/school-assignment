from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User


class DynamicFieldsSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class StudentBase(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_name', 'student_email', 'enrolled_year', 'student_status']


class TeacherBase(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_name', 'teacher_email', 'teacher_status']

'''
class StudentCourse(serializers.ModelSerializer):
    teachers = TeacherBase(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_status', 'teachers']


class TeacherCourse(serializers.ModelSerializer):
    students = StudentBase(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_status', 'students']
'''


class CourseSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    students = StudentBase(many=True, read_only=True)
    teachers = TeacherBase(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_status', 'students', 'teachers']


class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True, fields=('id', 'course_name', 'course_status', 'teachers'))

    class Meta:
        model = Student
        fields = ['id', 'student_name', 'student_email', 'enrolled_year', 'student_status', 'courses']


class TeacherSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'teacher_name', 'teacher_email', 'teacher_status', 'courses']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

