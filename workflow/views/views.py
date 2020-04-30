from django.shortcuts import render, redirect, reverse

from workflow.forms import UploadFileForm
from django.views.generic.edit import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from workflow import monitor
from metadata.imports import import_sessions, import_participants


@login_required
def workflow_view(request):
    return render(request, 'workflow/work_flow_view.html', {})


class MonitorImportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        context = {'form': UploadFileForm()}
        return render(request, 'workflow/util/monitor_import.html', context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if 'monitor_file' in request.FILES:
                monitor_file = request.FILES['monitor_file']
                monitor.import_(monitor_file)

            if 'sessions_file' in request.FILES:
                sessions_file = request.FILES['sessions_file']
                import_sessions.import_sessions(sessions_file)

            if 'participants_file' in request.FILES:
                participants_file = request.FILES['participants_file']
                import_participants.import_participants(participants_file)

            return redirect(reverse('workflow:monitor-import'))

        context = {'form': form}
        return render(request, 'workflow/util/monitor_import.html', context)
