from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from metadata import forms
from metadata.imports.import_languages import import_languages
from metadata.models import Language


def grouped(objs, n):
    for i in range(0, len(objs), n):
        yield objs[i:i + n]


@login_required
def language_list_view(request):
    languages = grouped(Language.objects.order_by('name'), 3)
    context = {'languages': languages}
    return render(request,
                  'metadata/language/language_list.html', context)


@login_required
def language_import_view(_):
    import_languages()
    return redirect('metadata:metadata-import')


@login_required
def language_create_view(request):
    language_form = forms.LanguageForm(request.POST or None)
    if language_form.is_valid():
        language_form.save()
        return redirect('metadata:language-list')
    context = {
        'language_form': language_form
    }
    return render(request, 'metadata/language/language_create.html', context)


@login_required
def language_update_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    language_form = forms.LanguageForm(request.POST or None, instance=language)
    if language_form.is_valid():
        language_form.save()
        return redirect('metadata:language-list')

    context = {'language_form': language_form}
    return render(request, 'metadata/language/language_update.html', context)


@login_required
def language_delete_view(_, pk):
    get_object_or_404(Language, pk=pk).delete()
    return redirect('metadata:language-list')
