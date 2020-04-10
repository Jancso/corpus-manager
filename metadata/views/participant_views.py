from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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
