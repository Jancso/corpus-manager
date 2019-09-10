from django import forms
from .models import Recording
import re


class RecordingForm(forms.ModelForm):

    class Meta:
        model = Recording
        fields = '__all__'

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'cols': 20
            }
        )
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        rgx = re.compile(r'deslas-[A-Z]{3,4}-\d{4}-\d{2}-\d{2}(-[A-Z0-9]+)?')

        if not rgx.fullmatch(name):
            raise forms.ValidationError(f'Format must be: /{rgx.pattern}/')

        return name