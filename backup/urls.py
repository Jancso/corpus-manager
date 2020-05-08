from django.urls import path

from backup.views import backup_view

app_name = 'backup'

urlpatterns = [
    path('', backup_view, name='backup-view')
]
