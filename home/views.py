from django.shortcuts import render


def home_detail_view(request):
    context = {}
    return render(request, 'home/home-detail.html', context)

