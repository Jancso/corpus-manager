import re

from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet, Form

from metadata.models import Recording, File, Session, Participant, \
    SessionParticipant, ParticipantLangInfo, Language, Role, Corpus, \
    CommunicationContext, Location, Project, Contact, Content, Access


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if hasattr(visible.field.widget, 'input_type'):
                widget_type = visible.field.widget.input_type

                if widget_type == 'text':
                    visible.field.widget.attrs['class'] = 'form-control'
                elif widget_type == 'checkbox':
                    visible.field.widget.attrs['class'] = 'form-check-input'
                elif widget_type == 'select':
                    visible.field.widget.attrs['class'] = 'form-select'
                else:
                    visible.field.widget.attrs['class'] = 'form-control'
            else:
                visible.field.widget.attrs['class'] = 'form-control'


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if hasattr(visible.field.widget, 'input_type'):
                widget_type = visible.field.widget.input_type

                if widget_type == 'text':
                    visible.field.widget.attrs['class'] = 'form-control'
                elif widget_type == 'checkbox':
                    visible.field.widget.attrs['class'] = 'form-check-input'
                elif widget_type == 'select':
                    visible.field.widget.attrs['class'] = 'form-select'
                else:
                    visible.field.widget.attrs['class'] = 'form-control'
            else:
                visible.field.widget.attrs['class'] = 'form-control'


class FileForm(BootstrapModelForm):
    class Meta:
        model = File
        fields = ['duration', 'size', 'location']


class SessionForm(BootstrapModelForm):
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


class ParticipantForm(BootstrapModelForm):
    class Meta:
        model = Participant
        exclude = ['anonymized']

    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')
        participants = Participant.objects.filter(anonymized=short_name)
        if participants:
            raise forms.ValidationError(
                f'Short name already used as anonymized code')
        if not short_name.isupper():
            raise forms.ValidationError(
                f'Short name has to be uppercase')
        return short_name


class ParticipantModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.short_name


class ParticipantRoleModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class SessionParticipantUpdateForm(BootstrapModelForm):
    roles = ParticipantRoleModelMultipleChoiceField(queryset=Role.objects.order_by('name'))

    class Meta:
        model = SessionParticipant
        fields = ['roles']


class SessionParticipantForm(BootstrapModelForm):
    def __init__(self, *args, session, **kwargs):
        self.session = session
        super().__init__(*args, **kwargs)

    participant = ParticipantModelChoiceField(queryset=Participant.objects.order_by('short_name'))
    roles = ParticipantRoleModelMultipleChoiceField(queryset=Role.objects.order_by('name'))

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


class ParticipantLangInfoForm(BootstrapModelForm):
    class Meta:
        model = ParticipantLangInfo
        exclude = ['participant']

    language = ParticipantLangModelMultipleChoiceField(queryset=Language.objects.order_by('name'))


class RecordingCreateForm(BootstrapModelForm):

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
            'language_speech', 'audio', 'notes']

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        rgx = re.compile(r'.*-[A-Z]{3,4}-\d{4}-\d{2}-\d{2}(-[A-Z0-9]+)?')

        if not rgx.fullmatch(name):
            raise forms.ValidationError(
                f'Format must be: /{rgx.pattern}/, i.e.'
                f'<corpus-name>-<shortname>-<date>(-<number>)'
            )

        return name


class RecordingMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UploadFileForm(BootstrapForm):
    corpus_file = forms.FileField(required=False)
    participants_file = forms.FileField(required=False)
    sessions_file = forms.FileField(required=False)
    monitor_file = forms.FileField(required=False)
    files_file = forms.FileField(required=False)


class RoleForm(BootstrapModelForm):
    class Meta:
        model = Role
        fields = '__all__'


class LanguageForm(BootstrapModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        labels = {'iso_code': 'ISO code'}


class ParticipantModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.short_name


class SessionFilterForm(BootstrapForm):
    name = forms.CharField(required=False)

    date_min = forms.DateField(required=False)
    date_max = forms.DateField(required=False)

    age_min = forms.CharField(max_length=7, initial='0')
    age_max = forms.CharField(max_length=7, initial='100')

    target_child = forms.CharField(max_length=4, required=False)

    participants = ParticipantModelMultipleChoiceField(
        queryset=Participant.objects.order_by('short_name'), required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            try:
                Session.objects.get(name=name)
            except Session.DoesNotExist:
                raise forms.ValidationError('Session does not exist!')

        return name

    def clean_age_min(self):
        age_min = self.cleaned_data.get('age_min')
        if age_min:
            if not re.fullmatch(r"(\d*)(;(\d*)(.(\d*))?)?", age_min):
                raise forms.ValidationError('Enter a valid age')
        return age_min

    def clean_age_max(self):
        age_max = self.cleaned_data.get('age_max')
        if age_max:
            if not re.fullmatch(r"(\d*)(;(\d*)(.(\d*))?)?", age_max):
                raise forms.ValidationError('Enter a valid age')
        return age_max


class CorpusGeneralForm(BootstrapModelForm):
    class Meta:
        model = Corpus
        fields = ['name']


class LocationForm(BootstrapModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class ProjectForm(BootstrapModelForm):
    class Meta:
        model = Project
        exclude = ['contact']


class ContactForm(BootstrapModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class ContentForm(BootstrapModelForm):
    class Meta:
        model = Content
        exclude = ['communication_context']


class CommunicationContextForm(BootstrapModelForm):
    class Meta:
        model = CommunicationContext
        fields = '__all__'


class AccessForm(BootstrapModelForm):
    class Meta:
        model = Access
        fields = '__all__'


class FileCreateForm(BootstrapModelForm):
    class Meta:
        model = File
        exclude = ['name']
