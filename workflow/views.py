from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Recording, Task, Assignment
from .forms import RecordingForm, TaskForm, UploadFileForm
from collections import namedtuple
from django.views.generic.edit import UpdateView, View
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import datetime


def _get_recs():
    Rec = namedtuple('Rec', ['pk', 'name', 'quality', 'status'])
    recs = []
    recordings = Recording.objects.all()

    for recording in recordings:
        tasks = Task.objects.filter(recording__name=recording.name)
        segmentation = tasks.filter(name=Task.SEGMENTATION).get()
        transcription = tasks.filter(name=Task.TRANSCRIPTION).get()
        glossing = tasks.filter(name=Task.GLOSSING).get()

        ordered_tasks = [segmentation, transcription, glossing]

        status = 'SOMETHING WENT WRONG'
        for task in ordered_tasks:
            if task.is_finished():
                if task == Task.GLOSSING:
                    status = 'FINISHED'
                    break
            else:
                status = \
                    f'{task.get_status_display()} {task.get_name_display()}'
                break

        recs.append(Rec(
            recording.pk,
            recording.name,
            recording.get_quality_display(),
            status
        ))

    return recs


def _get_assigned_tasks():
    assignments = Assignment.objects.all()
    filtered_assignments = []
    for assignment in assignments:
        if not assignment.task.is_finished():
            filtered_assignments.append(assignment)

    return filtered_assignments


def _get_open_tasks():
    tasks = []
    recordings = Recording.objects.all()

    for rec in recordings:
        segmentation = rec.task_set.filter(name=Task.SEGMENTATION).get()
        transcription = rec.task_set.filter(name=Task.TRANSCRIPTION).get()
        glossing = rec.task_set.filter(name=Task.GLOSSING).get()

        ordered_tasks = [segmentation, transcription, glossing]

        for pos, task in enumerate(ordered_tasks):
            if task.is_free():
                if pos == 0 or ordered_tasks[pos-1].is_finished():
                    tasks.append(task)
                    break

    return tasks


@login_required
def workflow_view(request):
    context = {
        'recordings': _get_recs(),
        'assigned_tasks': _get_assigned_tasks(),
        'open_tasks': _get_open_tasks()
    }
    return render(request, 'workflow/work_flow_view.html', context)


@login_required
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
    return render(request, 'workflow/recording/rec_create.html', context)


@login_required
def rec_detail_view(request, pk):
    rec = Recording.objects.get(pk=pk)
    segmentation = rec.task_set.filter(name=Task.SEGMENTATION).get()
    transcription = rec.task_set.filter(name=Task.TRANSCRIPTION).get()
    glossing = rec.task_set.filter(name=Task.GLOSSING).get()

    t = glossing.assignment_set

    context = {
        'recording': rec,
        'segmentation': segmentation,
        'transcription': transcription,
        'glossing': glossing,
    }
    return render(request, 'workflow/recording/rec_detail.html', context)


@login_required
@require_POST
def rec_delete_view(request, pk):
    rec = get_object_or_404(Recording, pk=pk)
    rec.delete()
    return redirect('workflow:workflow')


class RecordingUpdateView(LoginRequiredMixin, UpdateView):
    model = Recording
    template_name = 'workflow/recording/rec_update.html'
    form_class = RecordingForm

    def get_success_url(self):
        return reverse('workflow:rec-detail', args=(self.object.pk,))


class TaskUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task_form = TaskForm(instance=task)
        context = {
            'task': task,
            'form': task_form
        }
        return render(request, 'workflow/task/task_update.html', context)

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            if 'assignees' in task_form.changed_data and not task.start:
                task.start = datetime.datetime.today()
            task_form.save()

            if task.is_finished():
                task.end = datetime.datetime.today()

            if not task.is_finished():
                task.end = None

            if not task.assignment_set.all():
                task.start = None

            task.save()

            return redirect('workflow:rec-detail', pk=task.recording.pk)

        context = {
            'task': task,
            'form': task_form
        }
        return render(request, 'workflow/task/task_update.html', context)


class MonitorImportView(View):

    def import_monitor(self, file):
        pass

    def get(self, request):
        context = {'form': UploadFileForm()}
        return render(request, 'workflow/util/monitor_import.html', context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            self.import_monitor(request.FILES['file'])
            return redirect(reverse('workflow:workflow'))

        context = {'form': form}
        return render(request, 'workflow/util/monitor_import.html', context)
