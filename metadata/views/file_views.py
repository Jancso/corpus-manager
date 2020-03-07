from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import File


@login_required
def file_list_view(request):
    files = File.objects.all()
    context = {'files': files}
    return render(request, 'metadata/file/file_list.html', context)
