from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from workflow.models import Task


@login_required
def home_detail_view(request):
    user = request.user
    current_assignments = user.assignment_set.exclude(
        task__status__in=Task.finished_task_statuses)
    finished_assignments = user.assignment_set.filter(
        task__status__in=Task.finished_task_statuses)
    context = {
        'user': user,
        'current_assignments': current_assignments,
        'finished_assignments': finished_assignments
    }

    return render(request, 'home/home-detail.html', context)


@login_required
def settings_detail_view(request):
    return redirect('users:user-update', pk=request.user.pk)
