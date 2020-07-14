from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from metadata import forms
from metadata.imports.import_languages import import_languages
from metadata.models import Language, ParticipantLangInfo


def grouped(objs, n):
    return [objs[i:i + n] for i in range(0, len(objs), n)]


@login_required
def language_list_view(request):
    languages = grouped(Language.objects.order_by('name'), 4)
    context = {'languages': languages,
               'language_count': sum(1 for g in languages for _ in g)
               }
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
def language_delete_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    try:
        language.delete()
    except ProtectedError:
        participant_langs = ParticipantLangInfo.objects.filter(language=language)[:10]
        return render(request,
                      'metadata/language/language_delete_modal.html',
                      {'language': language,
                       'participant_langs': participant_langs})

    return redirect('metadata:language-list')
