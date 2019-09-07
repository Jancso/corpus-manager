from django.shortcuts import render


def home_detail_view(request):
    context = {'user': request.user}
    return render(request, 'home/home-detail.html', context)

