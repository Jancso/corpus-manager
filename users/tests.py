import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_GET_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

