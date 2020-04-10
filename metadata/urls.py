from django.urls import path

from metadata.views.rec_views import rec_delete_view, \
    RecordingUpdateView, rec_list_view
from metadata.views.views import metadata_view, metadata_create_view
from metadata.views.session_views import session_list_view, session_detail_view
from metadata.views.file_views import file_list_view

app_name = 'metadata'

urlpatterns = [
    path('', metadata_view, name='metadata-view'),

    path('create/', metadata_create_view, name='metadata-create'),

    path('sessions/', session_list_view, name='session-list'),
    path('sessions/<int:pk>/', session_detail_view, name='session-detail'),

    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),
    path('recordings/<int:pk>/update/', RecordingUpdateView.as_view(), name='rec-update'),

    path('files/', file_list_view, name='file-list')
]