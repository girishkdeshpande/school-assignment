from django.test import TestCase, Client
from django.urls import reverse
from ..models import *


class TestStudentList(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('students')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        # data = {
        #     'student_name': 'gogo',
        #     'student_email': 'gogo@example.com'
        # }

        response = self.client.post(self.url)

        # self.assertEquals(response.status_code, 201)


class TestCourseList(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class TestTeacherList(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('teachers')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
