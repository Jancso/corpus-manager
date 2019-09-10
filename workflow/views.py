from django.shortcuts import render, redirect
from .models import Recording, Task, Assignment
from .forms import RecordingForm
from collections import namedtuple


def workflow_view(request):
    Rec = namedtuple(
        'Rec',
        ['id', 'name', 'segmentation', 'transcription', 'glossing'])

    context = {
        'recordings': []
    }

    recordings = Recording.objects.all()

    for recording in recordings:
        tasks = Task.objects.filter(recording__name=recording.name)
        segmentation = tasks.filter(
            name=Task.SEGMENTATION).get().get_status_display()
        transcription = tasks.filter(
            name=Task.TRANSCRIPTION).get().get_status_display()
        glossing = tasks.filter(
            name=Task.GLOSSING).get().get_status_display()

        rec = Rec(recording.pk,
                  recording.name,
                  segmentation,
                  transcription,
                  glossing)

        context['recordings'].append(rec)

    return render(request, 'workflow/work_flow_view.html', context)


def rec_create_view(request):
    form = RecordingForm(request.POST or None)
    if form.is_valid():
        rec = form.save()
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.GLOSSING)

        return redirect('workflow:workflow')

    context = {
        'form': form
    }
    return render(request, 'workflow/rec_create.html', context)


# --------------------------------------

def assignments_list_view(request, task):
    context = {
        'working': [],
        'finished': [],
        'task': task
    }
    assignments = Assignment.objects.all()

    for assignment in assignments:

        if task == 'all' or assignment.task.name == task:
            if assignment.task.status in [
                    Task.STATUS_INCOMPLETE, Task.STATUS_COMPLETE]:
                context['finished'].append(assignment)
            else:
                context['working'].append(assignment)

    return render(request, 'workflow/assignment-list.html', context)
