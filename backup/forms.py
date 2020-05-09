from django import forms


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TokenForm(BootstrapForm):
    repository = forms.URLField()
    username = forms.CharField()
    token = forms.CharField()


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
