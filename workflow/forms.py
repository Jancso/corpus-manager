from django import forms
from .models import Recording, Task, Assignment
from django.contrib.auth.models import User
import re


class RecordingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Recording
        fields = '__all__'

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        rgx = re.compile(r'deslas-[A-Z]{3,4}-\d{4}-\d{2}-\d{2}(-[A-Z0-9]+)?')

        if not rgx.fullmatch(name):
            raise forms.ValidationError(f'Format must be: /{rgx.pattern}/')

        return name


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name


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
