from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from metadata import forms
from metadata.models import Corpus, CommunicationContext, Location, Project, Contact, Content


@login_required
def corpus_detail_view(request):
    if not Corpus.objects.exists():
        communication_context = CommunicationContext.objects.create()
        content = Content.objects.create(
            communication_context=communication_context)
        location = Location.objects.create()
        contact = Contact.objects.create()
        project = Project.objects.create(contact=contact)
        corpus = Corpus.objects.create(
            name='My Corpus',
            project=project,
            content=content,
            location=location
        )
    else:
        corpus = Corpus.objects.first()
    context = {'corpus': corpus}
    return render(request, 'metadata/corpus/corpus_detail.html', context)


class CorpusUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'metadata/corpus/corpus_update.html'
    success_url = reverse_lazy('metadata:corpus-detail')


class CorpusGeneralUpdate(CorpusUpdateView):
    model = Corpus
    form_class = forms.CorpusGeneralForm


class CorpusLocationUpdate(CorpusUpdateView):
    model = Location
    form_class = forms.LocationForm


class CorpusProjectUpdate(CorpusUpdateView):
    model = Project
    form_class = forms.ProjectForm


class CorpusContentUpdate(CorpusUpdateView):
    model = Content
    form_class = forms.ContentForm


class CorpusCommunicationContextUpdate(CorpusUpdateView):
    model = CommunicationContext
    form_class = forms.CommunicationContextForm


class CorpusContactUpdate(CorpusUpdateView):
    model = Contact
    form_class = forms.ContactForm
