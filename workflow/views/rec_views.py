from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import Recording
from workflow.models import Task, Discussion


def _get_recs():
    Rec = namedtuple('Rec', ['pk', 'name', 'quality', 'task', 'status'])
    recs = []
    recordings = Recording.objects.all()

    for recording in recordings:
        tasks = recording.task_set.all()
        segmentation = tasks.filter(name=Task.SEGMENTATION).get()
        transcription = tasks.filter(name=Task.TRANSCRIPTION).get()
        glossing = tasks.filter(name=Task.GLOSSING).get()

        ordered_tasks = [segmentation, transcription, glossing]

        status = 'SOMETHING WENT WRONG'
        task_name = 'SOMETHING WENT WRONG'
        for task in ordered_tasks:
            if task.is_finished():
                if task.name == Task.GLOSSING:
                    task_name = 'FINISHED'
                    status = 'FINISHED'
                    break
            else:
                task_name = task.get_name_display()
                status = task.get_status_display()
                break

        recs.append(Rec(
            recording.pk,
            recording.name,
            recording.get_quality_display(),
            task_name,
            status
        ))

    return recs


@login_required
def rec_list_view(request):
    context = {'recordings': _get_recs()}
    return render(request, 'workflow/recording/rec_list.html', context)


@login_required
def rec_detail_view(request, pk):
    rec = Recording.objects.get(pk=pk)
    segmentation = rec.task_set.filter(name=Task.SEGMENTATION).get()
    transcription = rec.task_set.filter(name=Task.TRANSCRIPTION).get()
    glossing = rec.task_set.filter(name=Task.GLOSSING).get()

    discussions = Discussion.objects.filter(recordings=pk)

    context = {
        'recording': rec,
        'segmentation': segmentation,
        'transcription': transcription,
        'glossing': glossing,
        'discussions': discussions
    }
    return render(request, 'workflow/recording/rec_detail.html', context)