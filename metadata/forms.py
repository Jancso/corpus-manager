import re

from django import forms

from metadata.models import Recording, File


class FileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = File
        fields = ['duration', 'size', 'location']


class RecordingCreateForm(forms.ModelForm):

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