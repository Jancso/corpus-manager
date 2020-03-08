
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from metadata.models import Recording, Session
from workflow.models import Task


class TaskTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

        session = Session.objects.create(
            name='deslas-AAA-2000-01-01', date='2000-01-01')

        rec = Recording.objects.create(
            name='deslas-AAA-2000-01-01', session=session)
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

    def test_task_1_update(self):
        response = self.c.get('/workflow/tasks/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_open_tasks(self):
        response = self.c.get('/workflow/tasks/open')
        self.assertEqual(response.status_code, 200)

    def test_assigned_tasks(self):
        response = self.c.get('/workflow/tasks/assigned')
        self.assertEqual(response.status_code, 200)