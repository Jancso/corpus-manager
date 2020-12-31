from django.forms import ModelForm, ImageField, FileInput
from .models import User


class BootstrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'file':
                visible.field.widget.attrs['class'] = 'form-control-file btn btn-secondary'
            else:
                visible.field.widget.attrs['class'] = 'form-control'


class UserForm(BootstrapForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image', 'job_function']

    image = ImageField(widget=FileInput, required=False)
