from django.test import TestCase, Client
from django.urls import reverse
from ..models import *


class TestStudentList(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('students')
        self.success_data = {
            'student_name': 'gogo',
            'student_email': 'gogo@example.com'
        }

        self.name_unsuccess_data = {
            'student_name': '*&^%$#@!',
            'student_email': 'gogo@example.com'
        }

        self.email_unsuccess_data = {
            'student_name': 'gogo',
            'student_email': '*&^%$!$#@example.com'
        }

        self.number_unsuccess_data = {
            'student_name': '23456',
            'student_email': '*&^%$!$#@example.com'
        }

        self.no_name = {
            'student_name': '',
            'student_email': 'gogo@example.com'
        }

        self.no_email = {
            'student_name': 'gogo',
            'student_email': ''
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_success(self):
        response = self.client.post(self.url, data=self.success_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_name_unsuccess(self):
        response = self.client.post(self.url, data=self.name_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_email_unsuccess(self):
        response = self.client.post(self.url, data=self.email_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_number_unsuccess(self):
        response = self.client.post(self.url, data=self.number_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_no_name(self):
        response = self.client.post(self.url, data=self.no_name, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_no_email(self):
        response = self.client.post(self.url, data=self.no_email, format='json')
        self.assertEqual(response.status_code, 406)


class TestCourseList(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course')
        self.success_data = {
            'course_name': 'azure'
        }

        self.unsuccess_data = {
            'course_name': '*&^%$#@'
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_success(self):
        response = self.client.post(self.url, data=self.success_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_unsuccess(self):
        response = self.client.post(self.url, data=self.unsuccess_data, format='json')
        self.assertEqual(response.status_code, 406)


class TestTeacherList(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('teachers')
        self.success_data = {
            'teacher_name': 'goga',
            'teacher_email': 'goga@example.com'
        }

        self.name_unsuccess_data = {
            'teacher_name': '*&^%$#@!',
            'teacher_email': 'goga@example.com'
        }

        self.email_unsuccess_data = {
            'teacher_name': 'goga',
            'teacher_email': '*&^%$!$#@example.com'
        }

        self.number_unsuccess_data = {
            'teacher_name': '23456',
            'teacher_email': '*&^%$!$#@example.com'
        }

        self.no_name = {
            'teacher_name': '',
            'teacher_email': 'gogo@example.com'
        }

        self.no_email = {
            'teacher_name': 'gogo',
            'teacher_email': ''
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_success(self):
        response = self.client.post(self.url, data=self.success_data, format='json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['teacher_email'], 'goga@example.com')

    def test_post_name_unsuccess(self):
        response = self.client.post(self.url, data=self.name_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_email_unsuccess(self):
        response = self.client.post(self.url, data=self.email_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_number_unsuccess(self):
        response = self.client.post(self.url, data=self.number_unsuccess_data, format='jason')
        self.assertEqual(response.status_code, 406)

    def test_post_no_name(self):
        response = self.client.post(self.url, data=self.no_name, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_no_email(self):
        response = self.client.post(self.url, data=self.no_email, format='json')
        self.assertEqual(response.status_code, 406)
