from django.urls import path

from backup.views import backup_view, TokenCreateView

app_name = 'backup'

urlpatterns = [
    path('', backup_view, name='backup-view'),
    path('token/create/', TokenCreateView.as_view(), name='token-create-view'),
]
