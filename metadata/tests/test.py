from django.test import TestCase
from django.test import Client

from users.models import User


class MetadataTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    def test_metdata(self):
        response = self.c.get('/metadata/')
        self.assertEqual(response.status_code, 200)
