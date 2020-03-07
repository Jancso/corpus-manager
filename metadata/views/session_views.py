from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import Session


@login_required
def session_list_view(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions}
    return render(request, 'metadata/session/session_list.html', context)
