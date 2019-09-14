from django.views import View
from django.views.generic.detail import DetailView
from .forms import UserForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'


class UserListView(LoginRequiredMixin, View):

    template_name = 'users/user_list.html'

    def grouped(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def get(self, request):
        context = {'object_list': self.grouped(User.objects.all(), 4)}
        return render(request, self.template_name, context)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    template_name = 'users/user_update.html'
    user_form = UserForm
    user_profile_form = UserProfileForm

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def get_user(self, pk):
        user = None
        if pk is not None:
            user = get_object_or_404(User, id=pk)

        return user

    def get(self, request, pk):
        context = {}
        user = self.get_user(pk)
        if user is not None:
            context['form'] = {
                'user': self.user_form(
                    instance=user),
                'user_profile': self.user_profile_form(
                    instance=user.userprofile)
            }

            context['user'] = user

        return render(request, self.template_name, context)

    def post(self, request, pk):
        context = {}
        user = self.get_user(pk)
        if user is not None:
            user_form = self.user_form(
                request.POST, instance=user)
            user_profile_form = self.user_profile_form(
                request.POST, request.FILES, instance=user.userprofile)

            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                user_profile_form.save()

            context['form'] = {
                'user': user_form,
                'user_profile': user_profile_form
            }

            context['user'] = user

        return render(request, self.template_name, context)
