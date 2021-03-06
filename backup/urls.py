from django.urls import path

from backup.views import backup_view, SSHKeyCreateView, RepositoryCreateView, \
    SchedulerCreateView, backup_create_view, download_backup_view

app_name = 'backup'

urlpatterns = [
    path('', backup_view, name='backup-view'),
    #path('create/', backup_create_view, name='backup-create'),
    #path('ssh/create/', SSHKeyCreateView.as_view(), name='ssh-create-view'),
    #path('repository/create/', RepositoryCreateView.as_view(), name='repository-create-view'),
    #path('scheduler/create/', SchedulerCreateView.as_view(), name='scheduler-create-view'),
    path('download/', download_backup_view, name='backup-download')
]
