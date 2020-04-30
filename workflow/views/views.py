from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def workflow_view(request):
    return render(request, 'workflow/work_flow_view.html', {})
