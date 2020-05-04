import re

from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet

from metadata.models import Recording, File, Session, Participant, SessionParticipant, ParticipantLangInfo, Language


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


class ParticipantModelMultipleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.short_name


class SessionParticipantForm(BootstrapForm):
    def __init__(self, *args, session, **kwargs):
        self.session = session
        super().__init__(*args, **kwargs)

    participant = ParticipantModelMultipleChoiceField(queryset=Participant.objects.order_by('short_name'))

    class Meta:
        model = SessionParticipant
        fields = ['participant', 'roles']

    def clean_participant(self):
        participant = self.cleaned_data.get('participant')
        if SessionParticipant.objects.filter(session=self.session, participant=participant):
            raise forms.ValidationError('Participant already exists!')

        return participant


class SessionParticipantFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        participants = set()
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            participant = form.cleaned_data.get('participant')
            if participant in participants:
                raise forms.ValidationError('Same participant used twice.')
            participants.add(participant)


SessionParticipantFormset = formset_factory(SessionParticipantForm, extra=1, formset=SessionParticipantFormset)


class ParticipantLangModelMultipleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ParticipantLangInfoForm(BootstrapForm):
    class Meta:
        model = ParticipantLangInfo
        exclude = ['participant']

    language = ParticipantLangModelMultipleChoiceField(queryset=Language.objects.order_by('name'))


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


class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-file'

    participants_file = forms.FileField(required=False)
    sessions_file = forms.FileField(required=False)
    monitor_file = forms.FileField(required=False)
    files_file = forms.FileField(required=False)
