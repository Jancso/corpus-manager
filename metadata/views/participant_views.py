from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from metadata.forms import ParticipantForm

from metadata.models import Participant


@login_required
def participant_list_view(request):
    participants = Participant.objects.order_by('short_name')
    context = {'participants': participants}
    return render(request, 'metadata/participant/participant_list.html', context)


class ParticipantCreateView(CreateView):
    model = Participant
    template_name = 'metadata/participant/participant_create.html'
    fields = '__all__'
    success_url = reverse_lazy('metadata:participant-list')


@login_required
def participant_detail_view(request, pk):
    participant = Participant.objects.get(pk=pk)
    context = {'participant': participant}
    return render(request, 'metadata/participant/participant_detail.html', context)


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    template_name = 'metadata/participant/participant_update.html'
    form_class = ParticipantForm

    def get_success_url(self):
        return reverse_lazy('metadata:participant-detail', args=(self.object.pk,))


@login_required
@require_POST
def participant_delete_view(_, pk):
    session = get_object_or_404(Participant, pk=pk)
    session.delete()
    return redirect('metadata:participant-list')
