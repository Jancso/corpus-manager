from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from metadata.models import Session


class SessionTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

        rec = Session.objects.create(
            name='deslas-AAA-2000-01-01')