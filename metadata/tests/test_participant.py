from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


class SessionTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    def test_participant_list(self):
        response = self.c.get('/metadata/participants/')
        self.assertEqual(response.status_code, 200)
