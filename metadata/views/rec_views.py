import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from metadata.forms import RecordingCreateForm, RecordingUpdateForm
from metadata.models import Recording, Session, File
from workflow.models import Task


@login_required
def rec_detail_view(request, pk):
    recording = Recording.objects.get(pk=pk)
    context = {'recording': recording}
    return render(request, 'metadata/recording/rec_detail.html', context)


@login_required
def rec_list_view(request):
    recs = Recording.objects.all()
    context = {'recs': recs}
    return render(request, 'metadata/recording/rec_list.html', context)


@login_required
@require_POST
def rec_delete_view(request, pk):
    rec = get_object_or_404(Recording, pk=pk)
    rec.delete()
    return redirect('metadata:rec-list')


class RecordingUpdateView(LoginRequiredMixin, UpdateView):
    model = Recording
    template_name = 'metadata/recording/rec_update.html'
    form_class = RecordingUpdateForm

    def get_success_url(self):
        return reverse('metadata:rec-detail', args=(self.object.pk,))


def _get_session_name(rec_name):
    regex = re.compile(r'.*-[A-Z]{3,}-\d\d\d\d-\d\d-\d\d(-\d+)?')
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
def rec_create_view(request):
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
    return render(request, 'metadata/recording/rec_create.html', context)
