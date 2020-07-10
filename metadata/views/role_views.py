from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from metadata.imports.import_roles import import_roles
from metadata.models import Role, SessionParticipant
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


@login_required
def role_delete_view(request, pk):
    role = get_object_or_404(Role, pk=pk)
    try:
        role.delete()
    except ProtectedError:
        participants = SessionParticipant.objects.filter(roles__name__contains=role.name)[:10]
        return render(request,
                      'metadata/role/role_delete_modal.html',
                      {'role': role,
                       'participants': participants})

    return redirect('metadata:role-list')
