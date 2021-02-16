from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from metadata.forms import FileCreateForm
from metadata.models import File


@login_required
def file_list_view(request):
    files = File.objects.all()
    context = {'files': files}
    return render(request, 'metadata/file/file_list.html', context)


class FileCreateView(CreateView):
    model = File
    form_class = FileCreateForm
    template_name = 'metadata/file/file_create.html'
    success_url = reverse_lazy('metadata:file-list')

    def form_valid(self, form):
        rec_name = form.cleaned_data['recording'].name
        rec_format = form.cleaned_data['format']
        file_name = f'{rec_name}.{rec_format}'
        form.instance.name = file_name
        return super().form_valid(form)
