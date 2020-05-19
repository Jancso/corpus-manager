from django import forms


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RepoForm(BootstrapForm):
    repository = forms.CharField(label="Repository's URL")

    def clean_repository(self):
        repository_url = self.cleaned_data['repository']

        if not repository_url.startswith('git@'):
            raise forms.ValidationError("Not a SSH URL")

        return repository_url



class SchedulerForm(BootstrapForm):

    MODE_AUTOMATIC = 'automatic'
    MODE_MANUAL = 'manual'

    MODE_CHOICES = [
        (MODE_AUTOMATIC, MODE_AUTOMATIC),
        (MODE_MANUAL, MODE_MANUAL)
    ]

    mode = forms.ChoiceField(choices=MODE_CHOICES, initial=MODE_AUTOMATIC)

    INTERVAL_CHOICES = [
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly')
    ]

    interval = forms.ChoiceField(choices=INTERVAL_CHOICES)
