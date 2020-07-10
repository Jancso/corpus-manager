from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect

from metadata.imports.import_roles import import_roles
from metadata.models import Role
from metadata import forms


@permission_required('is_superuser')
def role_import_view(_):
    import_roles()
    return redirect('metadata:metadata-import')


@login_required
def role_list_view(request):
    return render(request,
                  'metadata/role/role_list.html',
                  {'roles': Role.objects.all().order_by('name')})


@login_required
def role_create_view(request):
    role_form = forms.RoleForm(request.POST or None)
    if role_form.is_valid():
        role_form.save()
        return redirect('metadata:role-list')
    context = {
        'role_form': role_form
    }
    return render(request, 'metadata/role/role_create.html', context)
