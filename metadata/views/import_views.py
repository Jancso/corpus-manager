from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from metadata.imports import import_participants


@login_required
def participants_import_view(_):
    import_participants.import_participants()
    return redirect('metadata:participant-list')
