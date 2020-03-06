from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView

from workflow.forms import DiscussionForm, CommentForm
from workflow.models import Discussion, Comment


@login_required
def discussion_list_view(request):
    discussions = Discussion.objects.order_by('-create_time')
    context = {'discussions': discussions}
    return render(request, 'workflow/forum/discussion_list.html', context)


@login_required
def discussion_create_view(request):
    form = DiscussionForm(request.POST or None)
    if form.is_valid():
        discussion = form.save(commit=False)
        discussion.author = request.user
        discussion.save()
        form.save_m2m()
        return redirect('workflow:discussion-list')

    context = {'form': form}
    return render(request, 'workflow/forum/discussion_create.html', context)


@login_required
def discussion_detail_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    new_form = CommentForm()
    if request.method == 'POST':
        comment = Comment()
        comment.discussion = discussion
        comment.author = request.user
        posted_form = CommentForm(request.POST, instance=comment)
        if posted_form.is_valid():
            posted_form.save()

    context = {'discussion': discussion, 'form': new_form}
    return render(request, 'workflow/forum/discussion_detail.html', context)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'workflow/forum/comment_update.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'workflow:discussion-detail',
            args=(self.object.discussion.pk,)) + f'#comment-{self.object.pk}'


class DisussionUpdateView(LoginRequiredMixin, UpdateView):
    model = Discussion
    template_name = 'workflow/forum/discussion_update.html'
    form_class = DiscussionForm

    def get_success_url(self):
        return reverse('workflow:discussion-detail', args=(self.object.pk,))