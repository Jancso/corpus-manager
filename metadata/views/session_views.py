from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import Session


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
