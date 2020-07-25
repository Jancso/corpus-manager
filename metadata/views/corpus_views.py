from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from metadata import forms
from metadata.models import Corpus, CommunicationContext


@login_required
def corpus_detail_view(request):
    if not Corpus.objects.exists():
        communication_context = CommunicationContext.objects.create()
        corpus = Corpus.objects.create(
            name='My Corpus',
            communication_context=communication_context
        )
    else:
        corpus = Corpus.objects.first()
    context = {'corpus': corpus}
    return render(request, 'metadata/corpus/corpus_detail.html', context)


@login_required
def corpus_update_view(request):
    corpus = Corpus.objects.first()
    corpus_form = forms.CorpusForm(request.POST or None, instance=corpus)
    communication_context_form = forms.CommunicationContextForm(
        request.POST or None, instance=corpus.communication_context)
    if corpus_form.is_valid() and communication_context_form.is_valid():
        corpus_form.save()
        communication_context_form.save()
        return redirect('metadata:corpus-detail')

    context = {'corpus_form': corpus_form,
               'communication_context_form': communication_context_form}
    return render(request, 'metadata/corpus/corpus_update.html', context)
