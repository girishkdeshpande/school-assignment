from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from rest_framework import status

from ..views import *


class TestUrls(SimpleTestCase):
    def test_student_list(self):
        url = reverse('students')
        self.assertEqual(resolve(url).func.view_class, StudentList)

    def test_student_detail(self):
        url = reverse('student', args=[1])
        self.assertEqual(resolve(url).func.view_class, StudentDetail)

    def test_student_custom(self):
        url = reverse('studentcourse')
        self.assertEqual(resolve(url).func.view_class, StudentCustom)

    def test_course_list(self):
        url = reverse('course')
        self.assertEqual(resolve(url).func.view_class, CourseList)

    def test_course_detail(self):
        url = reverse('courses/id', args=[1])
        self.assertEqual(resolve(url).func.view_class, CourseDetail)

    def test_teacher_list(self):
        url = reverse('teachers')
        self.assertEqual(resolve(url).func.view_class, TeacherList)

    def test_user_list(self):
        url = reverse('users')
        self.assertEqual(resolve(url).func.view_class, UserList)

    def test_teacher_detail(self):
        url = reverse('teacher', args=[1])
        self.assertEqual(resolve(url).func.view_class, TeacherDetail)

    def test_teacher_custom(self):
        url = reverse('teachercourse')
        self.assertEqual(resolve(url).func.view_class, TeacherCustom)

    def test_search_teacher(self):
        url = reverse('searchteacher')
        self.assertEqual(resolve(url).func.view_class, SearchTeacher)

    def test_search_student(self):
        url = reverse('searchstudent')
        self.assertEqual(resolve(url).func.view_class, SearchStudent)

    def test_search_course(self):
        url = reverse('searchcourse')
        self.assertEqual(resolve(url).func.view_class, SearchCourse)
