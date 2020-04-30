from metadata.imports import import_sessions, import_participants, import_monitor

from metadata.forms import UploadFileForm
from django.views.generic.edit import View
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse


@login_required
def metadata_view(request):
    return render(request, 'metadata/metadata_overview.html', {})


class MetadataImportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        context = {'form': UploadFileForm()}
        return render(request, 'metadata/metadata_import.html', context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if 'monitor_file' in request.FILES:
                monitor_file = request.FILES['monitor_file']
                import_monitor.import_monitor(monitor_file)

            if 'sessions_file' in request.FILES:
                sessions_file = request.FILES['sessions_file']
                import_sessions.import_sessions(sessions_file)

            if 'participants_file' in request.FILES:
                participants_file = request.FILES['participants_file']
                import_participants.import_participants(participants_file)

            return redirect(reverse('metadata:metadata-import'))

        context = {'form': form}
        return render(request, 'metadata/metadata_import.html', context)
