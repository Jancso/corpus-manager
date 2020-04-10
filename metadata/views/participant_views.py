from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import Participant


@login_required
def participant_list_view(request):
    participants = Participant.objects.all()
    context = {'participants': participants}
    return render(request, 'metadata/participant/participant_list.html', context)
