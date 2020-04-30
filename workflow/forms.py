from django import forms

from metadata.forms import RecordingMultipleChoiceField
from .models import Task, Assignment, Discussion, Comment
from metadata.models import Recording
from django.contrib.auth.models import User


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username


class TaskForm(forms.ModelForm):
    assignees = UserModelMultipleChoiceField(required=False,
                                             queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['assignees'] = [
                assignment.person.pk
                for assignment in kwargs['instance'].assignment_set.all()]

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.assignment_set.all().delete()
            for user in self.cleaned_data['assignees']:
                a = Assignment.objects.create(task=instance, person=user)
                instance.assignment_set.add(a)

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()

        return instance

    class Meta:
        model = Task
        fields = ['status']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        assignees = cleaned_data.get('assignees')

        if status in [Task.STATUS_NOT_STARTED, Task.STATUS_BARRED]:
            if assignees:
                raise forms.ValidationError(
                    'This task status is only allowed '
                    'when there are no assignees. '
                    'Either unassign everyone '
                    'or choose a different status.')

        return cleaned_data


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DiscussionForm(BootstrapForm):

    class Meta:
        model = Discussion
        fields = ['title', 'description', 'recordings']

    recordings = RecordingMultipleChoiceField(required=False,
                                              queryset=Recording.objects.order_by('name'),
                                              widget=forms.SelectMultiple(
                                                  attrs={'size': 10})
                                              )


class CommentForm(BootstrapForm):

    class Meta:
        model = Comment
        fields = ['description']

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4})
    )
