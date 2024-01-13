from django.test import TestCase
from rest_framework import status

from ..models import *


class TestStudentModel(TestCase):
    def test_get(self):
        url = 'http://127.0.0.1:8000/mbschool/students/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
