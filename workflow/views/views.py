from django.shortcuts import render, redirect, reverse

from workflow.forms import UploadFileForm
from django.views.generic.edit import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from workflow import monitor


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
            monitor.import_(request.FILES['file'])
            return redirect(reverse('workflow:workflow'))

        context = {'form': form}
        return render(request, 'workflow/util/monitor_import.html', context)


