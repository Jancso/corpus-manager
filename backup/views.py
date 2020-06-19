from pathlib import Path
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from backup.forms import RepoForm, SchedulerForm


BACKUP_DATA_DIR_PATH = Path('backup-data')
REPO_DIRNAME = 'backup-repo'
REPO_PATH = (BACKUP_DATA_DIR_PATH / REPO_DIRNAME).resolve()
GIT_PATH = REPO_PATH / '.git'
DB_PATH = Path('test.sqlite3').resolve()
SSH_KEY_PATH = Path.home() / '.ssh/' / 'corpus_manager'


def get_public_ssh_key():
    with open(SSH_KEY_PATH.with_suffix('.pub')) as f:
        return f.read()


def generate_ssh_key():
    cmd = f'ssh-keygen -t ed25519 -N "" -C "corpus_manager" -f {SSH_KEY_PATH}'
    subprocess.run(cmd, shell=True)


def ssh_key_exists():
    return SSH_KEY_PATH.is_file()


def backup_repo_exists():
    return REPO_PATH.is_dir()


@login_required
def backup_view(request):
    if backup_repo_exists() and ssh_key_exists():
        log_cmd = f'git --git-dir={GIT_PATH} log --pretty=format:"%h%x09%ad%x09%s"'
        print(log_cmd)
        proc = subprocess.run(log_cmd, shell=True, capture_output=True)
        logs = str(proc.stdout, 'utf-8').split('\n')

        commits = []
        for log in logs:
            commits.append(log.split('\t'))

        context = {
            'log': repr(commits),
            'public_key': get_public_ssh_key()
        }
        return render(request, 'backup/backup_overview_ok.html', context)

    return render(request, 'backup/backup_overview_nok.html', {})


class SSHKeyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        if not ssh_key_exists():
            generate_ssh_key()

        context = {'public_key': get_public_ssh_key()}

        return render(request, 'backup/sshkey_create.html', context)


class RepositoryCreateView(LoginRequiredMixin, View):
    template = 'backup/repository_create.html'

    def get(self, request):
        form = RepoForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = RepoForm(request.POST)
        if form.is_valid():
            repository_url = form.cleaned_data['repository']

            # clone the repository
            BACKUP_DATA_DIR_PATH.mkdir(exist_ok=True)
            clone_cmd = f'git clone {repository_url} {REPO_PATH}'
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