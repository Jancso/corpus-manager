from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from metadata.models import Session, SessionParticipant, Participant, Role


class SessionTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        cls.c = Client()
        cls.c.login(username='test', password='test')

    @staticmethod
    def dummy_session():
        return Session.objects.create(
            name='deslas-AAA-2000-01-01',
            date='2000-01-01',
        )

    @staticmethod
    def dummy_participant():
        return Participant.objects.create(
            short_name='AAA',
            anonymized='XXX',
        )

    @staticmethod
    def dummy_role():
        return Role.objects.create(
            name='child'
        )

    @staticmethod
    def dummy_session_participant():
        session = SessionTest.dummy_session()
        participant = SessionTest.dummy_participant()
        roles = [SessionTest.dummy_role()]
        p = SessionParticipant(
            session=session,
            participant=participant,
        )
        p.save()
        p.roles.set(roles)

        return p

    def test_session_list(self):
        response = self.c.get(
            reverse('metadata:session-list'))
        self.assertEqual(response.status_code, 200)

    def test_session_detail(self):
        response = self.c.get(
            reverse('metadata:session-detail',
                    args=[self.dummy_session().pk]))
        self.assertEqual(response.status_code, 200)

    def test_session_update(self):
        response = self.c.get(
            reverse('metadata:session-update',
                    args=[self.dummy_session().pk]))
        self.assertEqual(response.status_code, 200)

    def test_session_delete(self):
        response = self.c.post(
            reverse('metadata:session-delete',
                    args=[self.dummy_session().pk]))
        self.assertEqual(response.status_code, 302)

    def test_session_participants_create(self):
        response = self.c.get(
            reverse('metadata:session-participants-create',
                    args=[self.dummy_session().pk]))
        self.assertEqual(response.status_code, 200)

    def test_session_participant_delete(self):
        session_participant = self.dummy_session_participant()
        response = self.c.post(
            reverse('metadata:session-participant-delete',
                    args=[session_participant.session.pk,
                          session_participant.pk]))
        self.assertEqual(response.status_code, 302)

    def test_session_participant_update(self):
        session_participant = self.dummy_session_participant()
        response = self.c.get(
            reverse('metadata:session-participant-update',
                    args=[session_participant.session.pk,
                          session_participant.pk]))
        self.assertEqual(response.status_code, 200)
