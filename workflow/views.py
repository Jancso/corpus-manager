from django.shortcuts import render, redirect
from .models import Recording, Task
from django.urls import reverse
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
        form.save()
        return redirect('workflow:workflow')

    context = {
        'form': form
    }
    return render(request, 'workflow/rec_create.html', context)
