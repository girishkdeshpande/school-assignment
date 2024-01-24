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
        data = response.json()
        self.assertIn('gogo', data['Student']['student_name'])
        self.assertIn('student_name', data['Student'])
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


class TestCourseDetails(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('courses/id', args=[1])
        self.data = Course.objects.create(
            course_name='python'
        )
        self.data_put_success = {
            'course_name': 'python with react'
        }
        self.data_put_unsuccess = {
            'course_name': 'python 3.11.5'
        }
        self.data_put_no_data = {
            'course_name': ''
        }

    def test_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_unsuccess(self):
        response = self.client.get(reverse('courses/id', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_put_success(self):
        response = self.client.put(self.url, data=self.data_put_success, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_unsuccess(self):
        response = self.client.put(self.url, data=self.data_put_unsuccess, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_put_no_data(self):
        response = self.client.put(self.url, data=self.data_put_no_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Course.objects.filter(id=self.data.id).exists())

    def test_delete_unsuccess(self):
        response = self.client.delete(reverse('courses/id', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_patch_success(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 200)

    def test_patch_unsuccess(self):
        response = self.client.get(self.url)
        response.data['course_status'] = False
        patch_record = self.client.patch(response)
        self.assertEqual(patch_record.status_code, 404)


class TestStudentDetails(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('student', args=[1])
        self.data = Student.objects.create(
            student_name='gayatri',
            student_email='gayatri@example.com'
        )
        self.data_put_success = {
            'student_name': 'gayatree',
            'student_email': 'gayatri@example.com'
        }
        self.data_put_unsuccess_name = {
            'student_name': 'gaya%$#',
            'student_email': 'gayatri@example.com'
        }
        self.data_put_unsuccess_email = {
            'student_name': 'gayatri',
            'student_email': 'ga%$#&*tri@example.com'
        }
        self.data_put_no_data = {
            'student_name': '',
            'student_email': ''
        }

    def test_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_unsuccess(self):
        response = self.client.get(reverse('student', args=[5]))
        self.assertEqual(response.status_code, 404)

    def test_put_success(self):
        response = self.client.put(self.url, data=self.data_put_success, content_type='application/json')
        self.assertEqual(response.status_code, 202)

    def test_put_unsuccess_name(self):
        response = self.client.put(self.url, data=self.data_put_unsuccess_name, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_put_unsuccess_email(self):
        response = self.client.put(self.url, data=self.data_put_unsuccess_email, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_put_no_data(self):
        response = self.client.put(self.url, data=self.data_put_no_data, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Student.objects.filter(id=self.data.id).exists())

    def test_delete_unsuccess(self):
        response = self.client.delete(reverse('student', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_patch_success(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 204)

    def test_patch_unsuccess(self):
        response = self.client.get(self.url)
        response.data['student_status'] = False
        patch_record = self.client.patch(response)
        self.assertEqual(patch_record.status_code, 404)


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


class TestTeacherDetails(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('teacher', args=[1])
        self.data = Teacher.objects.create(
            teacher_name='gayatri',
            teacher_email='gayatri@example.com'
        )
        self.data_put_success = {
            'teacher_name': 'gayatree',
            'teacher_email': 'gayatri@example.com'
        }
        self.data_put_unsuccess_name = {
            'teacher_name': 'gaya%$#',
            'teacher_email': 'gayatri@example.com'
        }
        self.data_put_unsuccess_email = {
            'teacher_name': 'gayatri',
            'teacher_email': 'ga%$#&*tri@example.com'
        }
        self.data_put_no_data = {
            'teacher_name': '',
            'teacher_email': ''
        }

    def test_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_unsuccess(self):
        response = self.client.get(reverse('teacher', args=[5]))
        self.assertEqual(response.status_code, 404)

    def test_put_success(self):
        response = self.client.put(self.url, data=self.data_put_success, content_type='application/json')
        self.assertEqual(response.status_code, 202)

    def test_put_unsuccess_name(self):
        response = self.client.put(self.url, data=self.data_put_unsuccess_name, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_put_unsuccess_email(self):
        response = self.client.put(self.url, data=self.data_put_unsuccess_email, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_put_no_data(self):
        response = self.client.put(self.url, data=self.data_put_no_data, content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Teacher.objects.filter(id=self.data.id).exists())

    def test_delete_unsuccess(self):
        response = self.client.delete(reverse('teacher', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_patch_success(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 204)

    def test_patch_unsuccess(self):
        response = self.client.get(self.url)
        response.data['teacher_status'] = False
        patch_record = self.client.patch(response)
        self.assertEqual(patch_record.status_code, 404)


class TestStudentCustom(TestCase):
    def setUp(self):
        self.url = reverse('studentcourse')
        self.student = Student.objects.create(
            student_name='ganga',
            student_email='ganga@example.com'
        )
        self.course_data = [Course(course_name='python'), Course(course_name='java')]
        Course.objects.bulk_create(self.course_data)

        self.success_data = {'id': 1, 'courses': [1, 2]}
        self.failure_data = {'id': 1, 'courses': [1, 3]}
        self.no_student = {'id': 2, 'courses': [1, 2]}

    def test_student_custom_success(self):
        response = self.client.post(self.url, data=self.success_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_student_custom_fail(self):
        response = self.client.post(self.url, data=self.failure_data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_student_custom_no_student(self):
        response = self.client.post(self.url, data=self.no_student, format='json')
        self.assertEqual(response.status_code, 404)


class TestTeacherCustom(TestCase):
    def setUp(self):
        self.url = reverse('teachercourse')
        self.teacher = Teacher.objects.create(
            teacher_name='ganga',
            teacher_email='ganga@example.com'
        )
        self.course_data = [Course(course_name='python'), Course(course_name='java')]
        Course.objects.bulk_create(self.course_data)

        self.success_data = {'id': 1, 'courses': [1, 2]}
        self.failure_data = {'id': 1, 'courses': [1, 3]}
        self.no_teacher = {'id': 2, 'courses': [1, 2]}

    def test_teacher_custom_success(self):
        response = self.client.post(self.url, data=self.success_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_teacher_custom_fail(self):
        response = self.client.post(self.url, data=self.failure_data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_teacher_custom_no_student(self):
        response = self.client.post(self.url, data=self.no_teacher, format='json')
        self.assertEqual(response.status_code, 404)
