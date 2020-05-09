from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from backup.forms import TokenForm, SchedulerForm


@login_required
def backup_view(request):
    return render(request, 'backup/backup_overview.html', {})


class TokenCreateView(LoginRequiredMixin, View):
    template = 'backup/token_create.html'

    def get(self, request):
        form = TokenForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = TokenForm(request.POST)
        if form.is_valid():
            return redirect('backup:scheduler-create-view')

        context = {'form': form}
        return render(request, self.template, context)


class SchedulerCreateView(LoginRequiredMixin, View):
    template = 'backup/scheduler_create.html'

    def get(self, request):
        form = SchedulerForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = SchedulerForm(request.POST)
        if form.is_valid():
            return redirect('backup:backup-view')

        context = {'form': form}
        return render(request, self.template, context)
