from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from metadata.forms import ParticipantForm, ParticipantLangInfoForm
from django.views import View

from metadata.models import Participant, ParticipantLangInfo


@login_required
def participant_list_view(request):
    participants = Participant.objects.order_by('short_name')
    context = {'participants': participants}
    return render(request, 'metadata/participant/participant_list.html',
                  context)


class ParticipantCreateView(CreateView):
    model = Participant
    template_name = 'metadata/participant/participant_create.html'
    fields = '__all__'
    success_url = reverse_lazy('metadata:participant-list')


@login_required
def participant_detail_view(request, pk):
    participant = Participant.objects.get(pk=pk)
    context = {'participant': participant}
    return render(request, 'metadata/participant/participant_detail.html',
                  context)


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    template_name = 'metadata/participant/participant_update.html'
    form_class = ParticipantForm

    def get_success_url(self):
        return reverse_lazy('metadata:participant-detail',
                            args=(self.object.pk,))


@login_required
@require_POST
def participant_delete_view(_, pk):
    session = get_object_or_404(Participant, pk=pk)
    session.delete()
    return redirect('metadata:participant-list')


class ParticipantLangInfoCreateView(LoginRequiredMixin, View):
    template = 'metadata/participant/participant_lang_info_create.html'

    def get(self, request, pk):
        form = ParticipantLangInfoForm()
        context = {
            'pk': pk,
            'form': form
        }
        return render(request, self.template, context)

    def post(self, request, pk):
        form = ParticipantLangInfoForm(request.POST)
        if form.is_valid():
            participant = Participant.objects.get(pk=pk)
            language = form.cleaned_data.get('language')
            main = form.cleaned_data.get('main')
            first = form.cleaned_data.get('first')
            second = form.cleaned_data.get('second')

            ParticipantLangInfo.objects.create(
                participant=participant,
                language=language,
                main=main,
                first=first,
                second=second)

            return redirect('metadata:participant-detail', pk=pk)

        context = {
            'pk': pk,
            'form': form
        }
        return render(request, self.template, context)


@login_required
@require_POST
def participant_language_delete_view(_, ppk, lpk):
    participant_lang_info = get_object_or_404(ParticipantLangInfo, pk=lpk)
    participant_lang_info.delete()
    return redirect('metadata:participant-detail', pk=ppk)


class ParticipantLangUpdateView(LoginRequiredMixin, View):

    def get(self, request, ppk, lpk):
        participant_lang_info = ParticipantLangInfo.objects.get(pk=lpk)
        form = ParticipantLangInfoForm(instance=participant_lang_info)
        context = {
            'participant_lang_info': participant_lang_info,
            'form': form
        }
        return render(request, 'metadata/participant/participant_language_update.html', context)

    def post(self, request, ppk, lpk):
        participant_lang_info = ParticipantLangInfo.objects.get(pk=lpk)
        form = ParticipantLangInfoForm(request.POST, instance=participant_lang_info)

        if form.is_valid():
            form.save()
            return redirect('metadata:participant-detail', pk=ppk)

        context = {
            'participant_lang_info': participant_lang_info,
            'form': form
        }
        return render(request, 'metadata/participant/participant_language_update.html', context)
