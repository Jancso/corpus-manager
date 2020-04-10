import re

from django import forms

from metadata.models import Recording, File, Session, Participant


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FileForm(BootstrapForm):
    class Meta:
        model = File
        fields = ['duration', 'size', 'location']


class SessionForm(BootstrapForm):
    class Meta:
        model = Session
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        date = cleaned_data.get('date')

        if name and date:
            if str(date) not in name:
                raise forms.ValidationError(
                    'Dates in session name and date field do not match.')


class ParticipantForm(BootstrapForm):
    class Meta:
        model = Participant
        fields = '__all__'


class RecordingCreateForm(BootstrapForm):

    FILES_WAV = 'wav'
    FILES_MOV = 'mov'
    FILES_MTS = 'mts'
    FILES_MP4 = 'mp4'

    FILES_CHOICES = [
        (FILES_WAV, 'WAV'),
        (FILES_MTS, 'MTS'),
        (FILES_MOV, 'MOV'),
        (FILES_MP4, 'MP4'),
    ]

    files = forms.MultipleChoiceField(choices=FILES_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Recording
        fields = [
            'name', 'quality', 'child_speech', 'directedness',
            'dene_speech', 'audio', 'notes']

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


class RecordingMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name