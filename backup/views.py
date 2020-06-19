from pathlib import Path
import shutil
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from backup.forms import RepoForm, SchedulerForm


BACKUP_DATA_DIR_PATH = Path('backup-data')
REPO_DIRNAME = 'backup-repo'
REPO_PATH = (BACKUP_DATA_DIR_PATH / REPO_DIRNAME).resolve()
DB_NAME = 'test'
DB_PATH = Path(DB_NAME + '.sqlite3').resolve()
SSH_KEY_PATH = Path.home() / '.ssh/' / 'corpus_manager'
COMMIT_MSG = 'Backup database'


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


def get_remote_url():
    remote_cmd = f'git -C {REPO_PATH} remote -v'
    proc = subprocess.run(remote_cmd, shell=True, capture_output=True)
    ssh_url = str(proc.stdout, 'utf-8').split(' ')[0][7:]
    repo = ssh_url.split(':')[1]
    https_url = f'https://gitlab.com/{repo}'

    return https_url


def get_sha_url(sha):
    remote_url = get_remote_url()[:-4]
    return Path(remote_url) / '-' / 'commit' / sha


def get_commits():
    log_cmd = f'git -C {REPO_PATH} log --pretty=format:"%H%x09%ad%x09%s"'
    proc = subprocess.run(log_cmd, shell=True, capture_output=True)
    logs = str(proc.stdout, 'utf-8').split('\n')
    commits = []
    for log in logs:
        sha, date, msg = log.split('\t')
        sha_url = get_sha_url(sha)
        commits.append({'sha': sha, 'sha_url': sha_url, 'date': date})
    return commits


def backup():
    sqlite3_path = Path(shutil.copy(DB_PATH, REPO_PATH))
    sql_path = sqlite3_path.with_suffix('.sql')

    csv_conversion_cdm = f'sqlite3 {sqlite3_path} .dump > {sql_path}'
    subprocess.run(csv_conversion_cdm, shell=True)

    add_cmd = f'git -C {REPO_PATH} add -v {sql_path.name}'
    subprocess.run(add_cmd, shell=True, capture_output=True)
    commit_cmd = f'git -C {REPO_PATH} commit -m "{COMMIT_MSG}"'
    subprocess.run(commit_cmd, shell=True)
    push_cmd = f'git -C {REPO_PATH} push'
    subprocess.run(push_cmd, shell=True)


def backup_create_view(request):
    backup()
    return redirect('backup:backup-view')


@login_required
def backup_view(request):
    if backup_repo_exists() and ssh_key_exists():
        commits = get_commits()
        repository = get_remote_url()

        context = {
            'repository': repository,
            'commits': commits,
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

            return redirect('backup:backup-view')

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
