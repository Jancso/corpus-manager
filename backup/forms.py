from django import forms


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TokenForm(BootstrapForm):
    username = forms.CharField()
    token = forms.CharField()


