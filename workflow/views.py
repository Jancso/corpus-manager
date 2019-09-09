from django.shortcuts import render
from .models import Recording, Task


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

