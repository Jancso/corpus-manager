import django_filters

from metadata.models import Session


class BootstrapFilter(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)

        for filter in self.filters:
            self.filters[filter].field.widget.attrs.update(
            {'class': 'form-control',
             'placeholder': filter.title()})


class SessionFilter(BootstrapFilter):
    class Meta:
        model = Session
        fields = ['name', 'date']
