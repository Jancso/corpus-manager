from pathlib import Path
import configparser
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from backup.forms import RepoForm, SchedulerForm


@login_required
def backup_view(request):
    return render(request, 'backup/backup_overview.html', {})


class SSHKeyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        ssh_key_path = Path.home() / '.ssh/' / 'corpus_manager'
        if not ssh_key_path.is_file():
            cmd = f'ssh-keygen -t ed25519 -N "" -C "corpus_manager" -f {ssh_key_path}'
            subprocess.run(cmd, shell=True)

        public_key = open(ssh_key_path.with_suffix('.pub')).read()
        context = {'public_key': public_key}

        return render(request, 'backup/sshkey_create.html', context)


class RepositoryCreateView(LoginRequiredMixin, View):
    template = 'backup/repository_create.html'

    BACKUP_DATA_DIR_PATH = Path('backup-data')
    REPO_DIRNAME = 'backup-repo'

    def get(self, request):
        form = RepoForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = RepoForm(request.POST)
        if form.is_valid():
            repository_url = form.cleaned_data['repository']

            # clone the repository
            self.BACKUP_DATA_DIR_PATH.mkdir(exist_ok=True)
            repository_path = (self.BACKUP_DATA_DIR_PATH / self.REPO_DIRNAME).resolve()
            clone_cmd = f'git clone {repository_url} {repository_path}'
            subprocess.run(clone_cmd, shell=True)

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
