import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from metadata.models import Recording
from workflow.forms import TaskForm
from workflow.models import Assignment, Task


def _get_assigned_tasks():
    assignments = Assignment.objects.all()
    filtered_assignments = []
    for assignment in assignments:
        if not assignment.task.is_finished():
            filtered_assignments.append(assignment)

    return filtered_assignments


@login_required
def assigned_task_list_view(request):
    context = {'assignments': _get_assigned_tasks(),
               'title': 'Assigned Tasks'}
    return render(request, 'workflow/assignment/assignment_list.html', context)


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
                if pos == 0 or ordered_tasks[pos - 1].is_finished():
                    tasks.append(task)
                    break

    return tasks


@login_required
def open_task_list_view(request):
    context = {'tasks': _get_open_tasks(),
               'title': 'Open Tasks'}
    return render(request, 'workflow/task/task_list.html', context)


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