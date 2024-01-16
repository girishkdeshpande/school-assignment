from .models import *
from .serializer import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import Token
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

import re
import logging

logger = logging.getLogger('django')

special_str = re.compile('[@_!#$%^&*()<>?\,;"/}|{~:0-9]')
number_only = re.compile('[@_!#$%^&*()<>?\,;"/}|{~:a-zA-Z]')
email_str = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"


# Student APIs
class StudentList(APIView):
    authentication_classes = (TokenAuthentication,)

    # View all student
    def get(self, request):
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response({'Students': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('No Records')
            return Response({"Error": 'No Records'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Enroll new student
    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            if special_str.search(request.data['student_name']):
                logger.error('Name should have characters only')
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['student_email']):
                logger.error('Invalid email id')
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Saved record - {serializer.data}')
                return Response({'Student': serializer.data}, status=status.HTTP_201_CREATED)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDetail(APIView):
    authentication_classes = (TokenAuthentication,)

    # View student by id
    def get(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response({'Student': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update student record
    def put(self, request, pk):
        logger.info(f'Input - {pk} {request.data}')
        try:
            if special_str.search(request.data['student_name']):
                logger.error('Name should have characters only')
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['student_email']):
                logger.error('Invalid email id')
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Student': serializer.data, 'Message': 'Record updated'},
                                status=status.HTTP_202_ACCEPTED)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist:
            logger.info('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete student record
    def delete(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete student
    def patch(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            student = Student.objects.get(pk=pk)
            student.student_status = False
            student.save()
            serializer = StudentSerializer(student)
            return Response({'Student': serializer.data}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentCustom(APIView):
    authentication_classes = (TokenAuthentication,)

    # Assign course to student
    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            student = Student.objects.get(id=request.data['id'])
            if student:
                for course in request.data['courses']:
                    cors = Course.objects.get(id=course)
                    if cors:
                        # assign_course = Course.objects.get(id=course)
                        student.courses.add(Course.objects.get(id=course))

                    else:
                        return Response({'Message': f'Course {course} does not exist'}, status=status.HTTP_404_NOT_FOUND)

                return Response({'Message': 'Course assigned'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Student does not exist')
            return Response({'Error': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchStudent(APIView):
    def get(self, request):
        logger.info(f'Input - {request.data}')
        try:
            student = Student.objects.filter(student_name__icontains=request.data['student_name'])
            serializer = StudentSerializer(student, many=True)
            return Response({'Students': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Student does not exist')
            return Response({'Error': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(e)
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Course APIs
class CourseList(APIView):
    authentication_classes = (TokenAuthentication,)

    # View all course
    def get(self, request):
        try:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response({'Courses': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Records does not exist')
            return Response({'Error': 'Records does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # New Course
    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            if special_str.search(request.data['course_name']):
                logger.error("Name should have characters only")
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Course': serializer.data, 'Message': 'Created'}, status=status.HTTP_201_CREATED)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDetail(APIView):
    authentication_classes = (TokenAuthentication,)

    # View course by id
    def get(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response({'Courses': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Record not found')
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update Course
    def put(self, request, pk):
        logger.info(f'Input - {pk} {request.data}')
        try:
            if special_str.search(request.data['course_name']):
                logger.error("Name should have characters only")
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Details': serializer.data, 'Message': 'Record updated'}, status=status.HTTP_200_OK)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            logger.error('Record not found')
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete course
    def delete(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({'Message': 'Record delete'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            logger.error('Record not found')
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete course
    def patch(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            course = Course.objects.get(pk=pk)
            if course.course_status:
                course.course_status = False
                course.save()
                serializer = CourseSerializer(course)
                return Response({'Courses': serializer.data, 'Message': 'Course deleted'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Record not found')
            return Response({'Error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchCourse(APIView):
    def get(self, request):
        logger.info(f'Input - {request.data}')
        try:
            course = Course.objects.filter(course_name__icontains=request.data['course_name'])
            serializer = CourseSerializer(course, many=True)
            return Response({'Courses': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Course does not exist')
            return Response({'Error': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(e)
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Teacher APIs
class TeacherList(APIView):
    authentication_classes = (TokenAuthentication,)

    # View all teachers
    def get(self, request):
        try:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return Response({'Teachers': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('No Records')
            return Response({'Error': 'No Records'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # New Teacher
    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            if special_str.search(request.data['teacher_name']):
                logger.error("Name should have characters only")
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['teacher_email']):
                logger.error("Invalid email id")
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = TeacherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Teacher': serializer.data}, status=status.HTTP_200_OK)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherDetail(APIView):
    authentication_classes = (TokenAuthentication,)

    # View teacher by id
    def get(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response({'Teacher': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update teacher
    def put(self, request, pk):
        logger.info(f'Input - {pk} {request.data}')
        try:
            if special_str.search(request.data['teacher_name']):
                logger.error("Name should have characters only")
                return Response({'Error': "Name should have characters only"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if not re.match(email_str, request.data['teacher_email']):
                logger.error("Invalid email id")
                return Response({'Error': "Invalid email id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Teacher': serializer.data, 'Message': 'Record updated'},
                                status=status.HTTP_202_ACCEPTED)

            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete teacher
    def delete(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            teacher = Teacher.objects.get(pk=pk)
            teacher.delete()
            return Response({'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Soft delete teacher
    def patch(self, request, pk):
        logger.info(f'Input - {pk}')
        try:
            teacher = Teacher.objects.get(pk=pk)
            if teacher.teacher_status:
                teacher.teacher_status = False
                teacher.save()
                serializer = TeacherSerializer(teacher)
                return Response({'Detail': serializer.data, 'Message': 'Record deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherCustom(APIView):
    authentication_classes = (TokenAuthentication,)

    # Assign course to teacher
    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            teacher = Teacher.objects.get(id=request.data['id'])
            if teacher:
                for course in request.data['courses']:
                    cors = Course.objects.get(id=course)
                    if cors:
                        # assign_course = Course.objects.get(id=course)
                        teacher.courses.add(Course.objects.get(id=course))

                    else:
                        return Response({'Message': f'Course {course} does not exist'}, status=status.HTTP_404_NOT_FOUND)

                return Response({'Message': 'Course assigned'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Teacher does not exist')
            return Response({'Error': 'Teacher does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchTeacher(APIView):
    def get(self, request):
        logger.info(f'Input - {request.data}')
        try:
            teacher = Teacher.objects.filter(teacher_name__icontains=request.data['teacher_name'])
            serializer = TeacherSerializer(teacher, many=True)
            return Response({'Teachers': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Teacher does not exist')
            return Response({'Error': 'Teacher does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(e)
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(APIView):
    authentication_classes = (TokenAuthentication,)

    # View all users
    def get(self, request):
        try:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response({'Users': serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            logger.error('Record does not exist')
            return Response({'Error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        logger.info(f'Input - {request.data}')
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                password = make_password(request.data['password'])
                serializer.save(password=password)
                Token.objects.create(user_id=serializer.data['id'])
                return Response({'Message': serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.error(f'Error - {serializer.errors}')
                return Response({'Error': serializer.errors}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f'An unexpected error occurred - {e}')
            return Response({'Error': f'An unexpected error occurred - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





