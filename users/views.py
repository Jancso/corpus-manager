from django.views import View
from .forms import UserForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import UserProfile


class UserUpdateView(View):

    template_name = 'users/user_update.html'
    user_form = UserForm
    user_profile_form = UserProfileForm

    def get_object(self, pk):
        obj = None
        if pk is not None:
            obj = get_object_or_404(UserProfile, id=pk)

        return obj

    def get(self, request, pk):
        context = {}
        obj = self.get_object(pk)
        if obj is not None:
            context['form'] = {
                'user': self.user_form(instance=obj.user),
                'user_profile': self.user_profile_form(instance=obj)
            }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        context = {}
        obj = self.get_object(pk)
        if obj is not None:
            user_form = self.user_form(
                request.POST, instance=obj.user)
            user_profile_form = self.user_profile_form(
                request.POST, instance=obj)

            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                user_profile_form.save()

            context['form'] = {
                'user': user_form,
                'user_profile': user_profile_form
            }

        return render(request, self.template_name, context)
