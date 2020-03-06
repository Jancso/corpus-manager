from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from workflow.models import Discussion, Comment


class ForumTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

        discussion = Discussion.objects.create(
            title='Title', description='Description', author=user)
        Comment.objects.create(
            discussion=discussion, author=user, description='Description')

    def test_discussions(self):
        response = self.c.get('/workflow/discussions/')
        self.assertEqual(response.status_code, 200)

    def test_discussion_create(self):
        response = self.c.get('/workflow/discussions/create/')
        self.assertEqual(response.status_code, 200)

    def test_discussion_1(self):
        response = self.c.get('/workflow/discussions/1/')
        self.assertEqual(response.status_code, 200)

    def test_discussion_update(self):
        response = self.c.get('/workflow/discussions/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_comment_update(self):
        response = self.c.get('/workflow/comments/1/update/')
        self.assertEqual(response.status_code, 200)
