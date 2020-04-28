from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from metadata.imports import import_participants, import_sessions


@login_required
def participants_import_view(_):
    import_participants.import_participants()
    return redirect('metadata:participant-list')


@login_required
def sessions_import_view(_):
    import_sessions.import_sessions()
    return redirect('metadata:session-list')
