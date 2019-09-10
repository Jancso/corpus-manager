from django.shortcuts import render, redirect
from .models import Recording, Task
from .forms import RecordingForm


def workflow_view(request):
    recordings = Recording.objects.all()

    for recording in recordings:
        seg = Task.objects.filter(recording__name=recording.name)
        segmentation = seg.filter(name='S').get()
        recording.segmentation = segmentation.get_status_display()

    context = {
        'recordings': recordings
    }
    return render(request, 'workflow/work_flow_view.html', context)


def rec_create_view(request):
    form = RecordingForm(request.POST or None)
    if form.is_valid():
        rec = form.save()
        Task.objects.create(recording=rec, name=Task.SEGMENTATION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION)
        Task.objects.create(recording=rec, name=Task.TRANSCRIPTION_CHECK)
        Task.objects.create(recording=rec, name=Task.GLOSSING)
        Task.objects.create(recording=rec, name=Task.GLOSSING_CHECK)

        return redirect('workflow:workflow')

    context = {
        'form': form
    }
    return render(request, 'workflow/rec_create.html', context)
