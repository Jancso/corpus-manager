from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_detail_view(request):
    context = {'user': request.user}
    return render(request, 'home/home-detail.html', context)

