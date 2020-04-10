from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse

from metadata.models import Session
from metadata.forms import SessionForm


@login_required
def session_list_view(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions}
    return render(request, 'metadata/session/session_list.html', context)


@login_required
def session_detail_view(request, pk):
    session = Session.objects.get(pk=pk)
    recs = session.recording_set.all()
    context = {'session': session}
    return render(request, 'metadata/session/session_detail.html', context)


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = Session
    template_name = 'metadata/session/session_update.html'
    form_class = SessionForm

    def get_success_url(self):
        return reverse('metadata:session-detail', args=(self.object.pk,))
