import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView
from django.urls import reverse
from django.views.generic.base import View

from metadata.models import Session, SessionParticipant, Participant, SessionParticipantRole
from metadata.forms import SessionForm, SessionParticipantFormset, \
    SessionParticipantForm, SessionParticipantUpdateForm


@login_required
def session_list_view(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions}
    return render(request, 'metadata/session/session_list.html', context)


@login_required
def session_detail_view(request, pk):
    session = Session.objects.get(pk=pk)
    participants = SessionParticipant.objects.filter(session=session)
    context = {'session': session,
               'participants': participants}
    return render(request, 'metadata/session/session_detail.html', context)


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = Session
    template_name = 'metadata/session/session_update.html'
    form_class = SessionForm

    def get_success_url(self):
        return reverse('metadata:session-detail', args=(self.object.pk,))


class SessionParticipantUpdateView(LoginRequiredMixin, View):
    template = 'metadata/session/session_participant_update.html'

    def get(self, request, spk, ppk):
        session_participant = SessionParticipant.objects.get(pk=ppk)
        form = SessionParticipantUpdateForm(instance=session_participant)
        context = {'form': form, 'session_participant': session_participant}
        return render(request, self.template, context)

    def post(self, request, spk, ppk):
        session_participant = SessionParticipant.objects.get(pk=ppk)
        form = SessionParticipantUpdateForm(request.POST, instance=session_participant)

        if form.is_valid():
            form.save()
            return redirect('metadata:session-detail', pk=spk)

        context = {'form': form, 'session_participant': session_participant}
        return render(request, self.template, context)


@login_required
@require_POST
def session_delete_view(_, pk):
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    return redirect('metadata:session-list')


def session_participants_create_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == 'GET':
        formset = SessionParticipantFormset(request.GET or None, form_kwargs={'session': session})
    elif request.method == 'POST':
        formset = SessionParticipantFormset(request.POST, form_kwargs={'session': session})
        if formset.is_valid():
            for form in formset:
                participant = form.cleaned_data.get('participant')
                roles = form.cleaned_data.get('roles')
                if participant and session and roles:
                    session_participant = SessionParticipant(
                        participant=participant, session=session)
                    session_participant.save()
                    for role in roles:
                        SessionParticipantRole.objects.create(
                            session_participant=session_participant,
                            role=role
                        )

            return redirect('metadata:session-detail', pk=pk)

    return render(request, 'metadata/session/session_participants_create.html', {
        'formset': formset,
        'session': session
    })


@login_required
@require_POST
def session_participant_delete_view(_, spk, ppk):
    session_participant = get_object_or_404(SessionParticipant, pk=ppk)
    session_participant.delete()
    return redirect('metadata:session-detail', pk=spk)


@login_required
def session_csv_export(_):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sessions.csv"'

    fieldnames = [
        'Code',
        'Date',
        'Location',
        'Length of recording',
        'Situation',
        'Content',
        'Participants and roles',
        'Comments'
    ]

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for session in Session.objects.all():
        # fetch participants and roles
        participants = []
        for p in session.sessionparticipant_set.all():
            part_role = f'{p.participant.short_name} ({p.role})'
            participants.append(part_role)
        participants_and_roles = ', '.join(participants)

        writer.writerow({'Code': session.name,
                         'Date': session.date,
                         'Location': session.location,
                         'Length of recording': '',
                         'Situation': session.situation,
                         'Content': session.content,
                         'Participants and roles': participants_and_roles,
                         'Comments': session.comments})

    return response
