from django.test import TestCase
from django.urls import reverse
from django.test import Client
from users.models import User


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'this_is_secret'
        self.user = User.objects.create_user(
            'test', 'test@test.ch', self.password)

    def test_GET_user_list(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('users:user-list'))
        self.assertEqual(response.status_code, 200)

    def test_GET_user_detail(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('users:user-detail',
                                           args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_GET_user_update(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('users:user-update',
                                           args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
