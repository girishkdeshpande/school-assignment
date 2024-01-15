from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from rest_framework import status

from ..views import *


class TestUrls(SimpleTestCase):
    def test_student_list(self):
        url = reverse('students')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, StudentList)

    # def test_student_detail(self):
    #     url = reverse('student', args=['/<int:pk>'])
    #     print(resolve(url))
    #     self.assertEqual(resolve(url).fun.view_class, StudentDetail)

    def test_student_custom(self):
        url = reverse('studentcourse')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, StudentCustom)

    def test_course_list(self):
        url = reverse('course')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, CourseList)

    def test_teacher_list(self):
        url = reverse('teachers')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, TeacherList)

    # def test_student_detail(self):
    #     url = reverse('student', args=['/pk'])
    #     print(resolve(url))
    #     self.assertEqual(resolve(url).fun.view_class, StudentDetail)

    def test_teacher_custom(self):
        url = reverse('teachercourse')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, TeacherCustom)
