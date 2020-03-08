from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from metadata.forms import RecordingCreateForm
from metadata.models import Recording


@login_required
def rec_list_view(request):
    recs = Recording.objects.all()
    context = {'recs': recs}
    return render(request, 'metadata/recording/rec_list.html', context)


@login_required
@require_POST
def rec_delete_view(request, pk):
    rec = get_object_or_404(Recording, pk=pk)
    rec.delete()
    return redirect('workflow:workflow')


class RecordingUpdateView(LoginRequiredMixin, UpdateView):
    model = Recording
    template_name = 'metadata/recording/rec_update.html'
    form_class = RecordingCreateForm

    def get_success_url(self):
        return reverse('workflow:rec-detail', args=(self.object.pk,))