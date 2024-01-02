from django.http import HttpResponse, JsonResponse
from .models import Course, Student, Teacher
from .serializer import CourseSerializer, StudentSerializer, TeacherSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, viewsets


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
