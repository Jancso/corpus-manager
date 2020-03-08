import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from metadata.forms import RecordingCreateForm
from workflow.models import Task
from metadata.models import Recording, Session, File


@login_required
def metadata_view(request):
    return render(request, 'metadata/metadata_overview.html', {})


def _get_session_name(rec_name):
    regex = re.compile(r'deslas-[A-Z]{3,}-\d\d\d\d-\d\d-\d\d(-\d+)?')
    match = regex.search(rec_name)

    if match:
        return match.group()
    else:
        return None


def _get_session_date(session_name):
    regex = re.compile(r'\d\d\d\d-\d\d-\d\d')
    match = regex.search(session_name)

    if match:
        return match.group()
    else:
        return None


@login_required
def metadata_create_view(request):
    rec_form = RecordingCreateForm(request.POST or None)

    if rec_form.is_valid():

        # create/infer session
        rec_name = rec_form.cleaned_data['name']
        session_name = _get_session_name(rec_name)
        session_date = _get_session_date(session_name)
        session, _ = Session.objects.get_or_create(
            name=session_name, date=session_date)

        # set session for rec and save rec
        rec_form.instance.session = session
        rec = rec_form.save()

        # create tasks
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

        # create files
        for extension in rec_form.cleaned_data['files']:
            filename = f'{rec_name}.{extension}'
            File.objects.create(name=filename, recording=rec, format=extension)

        return redirect('metadata:rec-list')

    context = {
        'form': rec_form
    }
    return render(request, 'metadata/metadata_create.html', context)
