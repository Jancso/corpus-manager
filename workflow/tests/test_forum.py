from django.test import TestCase
from django.test import Client

from users.models import User
from workflow.models import Discussion, Comment


class ForumTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test')
        cls.user.set_password('test')
        cls.user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    def setUp(self):
        discussion = Discussion.objects.create(
            title='Title', description='Description', author=self.user)
        Comment.objects.create(
            discussion=discussion, author=self.user, description='Description')

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
