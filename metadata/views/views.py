from metadata.tasks import import_metadata
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
            import_metadata(request.FILES)
            return redirect(reverse('metadata:metadata-import'))

        context = {'form': form}
        return render(request, 'metadata/metadata_import.html', context)
