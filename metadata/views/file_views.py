from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from metadata.forms import FileCreateForm
from metadata.models import File


@login_required
def file_list_view(request):
    files = File.objects.all()
    context = {'files': files}
    return render(request, 'metadata/file/file_list.html', context)


@login_required
def file_delete_view(_, pk):
    rec = get_object_or_404(File, pk=pk)
    rec.delete()
    return redirect('metadata:file-list')


class FileCreateView(LoginRequiredMixin, CreateView):
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
