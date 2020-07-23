from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from metadata import forms
from metadata.models import Corpus


@login_required
def corpus_detail_view(request):
    if not Corpus.objects.exists():
        corpus = Corpus.objects.create(
            name='My Corpus'
        )
    else:
        corpus = Corpus.objects.first()
    context = {'corpus': corpus}
    return render(request, 'metadata/corpus/corpus_detail.html', context)


@login_required
def corpus_update_view(request):
    corpus = Corpus.objects.first()
    corpus_form = forms.CorpusForm(request.POST or None, instance=corpus)
    if corpus_form.is_valid():
        corpus_form.save()
        return redirect('metadata:corpus-detail')

    context = {'corpus_form': corpus_form}
    return render(request, 'metadata/corpus/corpus_update.html', context)
