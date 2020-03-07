from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


class MetadataTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

    def test_recording_create(self):
        response = self.c.get('/metadata/')
        self.assertEqual(response.status_code, 200)
