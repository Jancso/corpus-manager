from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from metadata.models import Recording
from workflow.models import Task


class RecordingTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

        rec = Recording.objects.create(name='deslas-AAA-2000-01-01')
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

    def test_workflow_recordings(self):
        response = self.c.get('/workflow/recordings/')
        self.assertEqual(response.status_code, 200)

