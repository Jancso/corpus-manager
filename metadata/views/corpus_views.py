from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from metadata import forms
from metadata.models import Corpus, CommunicationContext, Location, Project, Contact


@login_required
def corpus_detail_view(request):
    if not Corpus.objects.exists():
        communication_context = CommunicationContext.objects.create()
        location = Location.objects.create()
        contact = Contact.objects.create()
        project = Project.objects.create(contact=contact)
        corpus = Corpus.objects.create(
            name='My Corpus',
            project=project,
            communication_context=communication_context,
            location=location
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
    location_form = forms.LocationForm(
        request.POST or None, instance=corpus.location)
    contact_form = forms.ContactForm(
        request.POST or None, instance=corpus.project.contact)
    project_form = forms.ProjectForm(
        request.POST or None, instance=corpus.project)

    if corpus_form.is_valid() \
            and communication_context_form.is_valid() \
            and location_form.is_valid()\
            and contact_form.is_valid()\
            and project_form.is_valid():
        corpus_form.save()
        communication_context_form.save()
        location_form.save()
        contact_form.save()
        project_form.save()
        return redirect('metadata:corpus-detail')

    context = {'corpus_form': corpus_form,
               'communication_context_form': communication_context_form,
               'location_form': location_form,
               'contact_form': contact_form,
               'project_form': project_form
               }
    return render(request, 'metadata/corpus/corpus_update.html', context)
