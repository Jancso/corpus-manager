from django.test import TestCase
from django.test import Client

from metadata.models import Recording, Session
from users.models import User
from workflow.models import Task


class RecordingTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    def setUp(self):
        session = Session.objects.create(
            name='deslas-AAA-2000-01-01', date='2000-01-01')

        rec = Recording.objects.create(
            name='deslas-AAA-2000-01-01', session=session)
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

    def test_recording_update(self):
        response = self.c.get('/metadata/recordings/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_recording_list(self):
        response = self.c.get('/metadata/recordings/')
        self.assertEqual(response.status_code, 200)

    def test_recording_create(self):
        response = self.c.get('/metadata/recordings/create/')
        self.assertEqual(response.status_code, 200)
