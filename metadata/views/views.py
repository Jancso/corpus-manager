import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def metadata_view(request):
    return render(request, 'metadata/metadata_overview.html', {})
