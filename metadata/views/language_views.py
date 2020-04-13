from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from metadata.models import Language


@login_required
def language_list_view(request):
    languages = Language.objects.order_by('name')
    context = {'languages': languages}
    return render(request,
                  'metadata/language/language_list.html', context)
