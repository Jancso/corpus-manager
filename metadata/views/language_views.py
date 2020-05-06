from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from metadata.imports.import_languages import import_languages
from metadata.models import Language


@login_required
def language_list_view(request):
    languages = Language.objects.order_by('name')
    context = {'languages': languages}
    return render(request,
                  'metadata/language/language_list.html', context)


@login_required
def language_import_view(_):
    import_languages()
    return redirect('metadata:metadata-import')
