from django.views import View
from .forms import UserForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import User


class UserUpdateView(View):

    template_name = 'users/user_update.html'
    user_form = UserForm
    user_profile_form = UserProfileForm

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
