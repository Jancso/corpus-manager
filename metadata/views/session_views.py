from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView
from django.urls import reverse

from metadata.models import Session, SessionParticipant, Participant
from metadata.forms import SessionForm, SessionParticipantFormset


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
                # extract name from each form and save
                participant = form.cleaned_data.get('participant')
                role = form.cleaned_data.get('role')
                # save book instance
                if participant and session and role:
                    SessionParticipant(participant=participant, session=session, role=role).save()
            # once all books are saved, redirect to book list view
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
