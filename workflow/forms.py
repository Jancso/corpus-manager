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


class TaskForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['users'] = [t.person.pk for t in
                kwargs['instance'].assignment_set.all()]

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.assignment_set.all().delete()
            for user in self.cleaned_data['users']:
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
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if status in [Task.STATUS_NOT_STARTED, Task.STATUS_BARRED]:
            if start or end:
                raise forms.ValidationError(
                    'status only allowed '
                    'for tasks without assignees. '
                    'Unassign everyone for this task first.')

        return cleaned_data


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
