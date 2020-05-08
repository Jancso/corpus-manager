from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def backup_view(request):
    return render(request, 'backup/backup_overview.html', {})
