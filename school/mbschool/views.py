from .models import Course, Student, Teacher
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

import re

special_str = re.compile('[@_!#$%^&*()<>?\/}|{~:]')
email_str = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"


# Student APIs
class StudentList(APIView):

    # View all student
    def get(self, request):
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response({'Students': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"Error": 'No Records'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Enroll new student
    def post(self, request):
        try:
            if 'id' in request.data or 'student_status' in request.data:
                request.data.pop('id')
                request.data.pop('student_status')

            if special_str.search(request.data['student_name']):
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['student_email']):
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Student': serializer.data}, status=status.HTTP_201_CREATED)

            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error': f'An unexpected error occured - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDetail(APIView):

    # View student by id
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response({'Student': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'})

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update student record
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Student': serializer.data, 'Message': 'Record updated'},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'})

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete student record
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'})

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete student
    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.student_status = False
            student.save()
            return Response({'Student': student}, status=status.HTTP_202_ACCEPTED)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'})

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentCustom(APIView):
    pass


# Course APIs

class CourseList(APIView):
    # View all course
    def get(self, request):
        try:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response({'Courses': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'Error': 'No Records'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # New Course
    def post(self, request):
        try:
            if special_str.search(request.data['course_name']):
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Course': serializer.data, 'Message': 'Created'}, status=status.HTTP_201_CREATED)

            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDetail(APIView):
    # View course by id
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response({'Courses': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update Course
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Details': serializer.data, 'Message': 'Record updated'}, status=status.HTTP_200_OK)

            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete course
    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({'Message': 'Record delete'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete course
    def patch(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            if course.course_status:
                course.course_status = False
                course.save()
                return Response({'Courses': course, 'Message': 'Course deleted'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Teacher APIs
class TeacherList(APIView):
    # View all teachers
    def get(self, request):
        try:
            teachers = Teacher.objects.all()
            if teachers:
                serializer = TeacherSerializer(teachers, many=True)
                return Response({'Teachers': serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'Error': 'No Records'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # New Teacher
    def post(self, request):
        try:
            if special_str.search(request.data['teacher_name']):
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['teacher_email']):
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = TeacherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Teacher': serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherDetail(APIView):
    # View teacher by id
    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response({'Teacher': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update teacher
    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Teacher': serializer.data, 'Message': 'Record updated'}, status=status.HTTP_202_ACCEPTED)

            else:
                return Response({'Error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete teacher
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            teacher.delete()
            return Response({'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete teacher
    def patch(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            if teacher.teacher_status:
                teacher.teacher_status = False
                teacher.save()
                return Response({'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
