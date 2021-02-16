import io
import zipfile
from xml.etree.ElementTree import ElementTree

from django.http import HttpResponse
from lxml.etree import Element, tostring
import threading

from metadata.exports.IMDIMaker import IMDIMaker
from metadata.imports.import_metadata import import_metadata
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
            x = threading.Thread(target=import_metadata, args=(request.FILES,))
            x.start()
            return redirect(reverse('metadata:metadata-view'))

        context = {'form': form}
        return render(request, 'metadata/metadata_import.html', context)


@login_required
def imdi_export_view(request):
    imdi_maker = IMDIMaker(request.user)
    buffer = imdi_maker.generate_imdis()
    response = HttpResponse(buffer.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename="IMDI.zip"'
    return response
