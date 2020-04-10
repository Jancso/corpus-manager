from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from metadata.models import Session


class SessionTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    def setUp(self):
        Session.objects.create(
            name='deslas-AAA-2000-01-01',
            date='2000-01-01',
        )

    def test_session_list(self):
        response = self.c.get('/metadata/sessions/')
        self.assertEqual(response.status_code, 200)

    def test_session_detail(self):
        response = self.c.get('/metadata/sessions/1/')
        self.assertEqual(response.status_code, 200)

    def test_session_update(self):
        response = self.c.get('/metadata/sessions/1/update/')
        self.assertEqual(response.status_code, 200)
