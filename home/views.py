from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def home_detail_view(request):
    context = {'user': request.user}
    return render(request, 'home/home-detail.html', context)


@login_required
def settings_detail_view(request):
    return redirect('users:user-update', pk=request.user.userprofile.pk)
