from django.test import TestCase
from django.test import Client

from metadata.models import Session, Recording, File
from users.models import User
from workflow.models import Task

import datetime


class FileTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.c = Client()
        self.c.login(username='test', password='test')

        session = Session.objects.create(
            name='deslas-AAA-2000-01-01',
            date='2000-01-01',
        )

        rec = Recording.objects.create(
            name='deslas-AAA-2000-01-01',
            session=session
        )
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

        File.objects.create(
            name='deslas-AAA-2000-01-01.mov',
            recording=rec,
            type='A',
            format='mov',
            duration=datetime.timedelta(hours=1),
            size='100000000',
            location='/home/sweet/home'
        )

    def test_file_list(self):
        response = self.c.get('/metadata/files/')
        self.assertEqual(response.status_code, 200)
