from django.urls import path

from metadata.views.rec_views import rec_delete_view, \
    RecordingUpdateView, rec_list_view
from metadata.views.views import metadata_view, metadata_create_view
from metadata.views.session_views import session_list_view, session_detail_view, SessionUpdateView, session_delete_view
from metadata.views.file_views import file_list_view
from metadata.views.participant_views import participant_list_view, ParticipantCreateView, participant_detail_view

app_name = 'metadata'

urlpatterns = [
    path('', metadata_view, name='metadata-view'),

    path('create/', metadata_create_view, name='metadata-create'),

    path('sessions/', session_list_view, name='session-list'),
    path('sessions/<int:pk>/', session_detail_view, name='session-detail'),
    path('sessions/<int:pk>/update/', SessionUpdateView.as_view(), name='session-update'),
    path('sessions/<int:pk>/delete/', session_delete_view, name='session-delete'),

    path('participants/', participant_list_view, name='participant-list'),
    path('participants/create/', ParticipantCreateView.as_view(), name='participant-create'),
    path('participants/<int:pk>/', participant_detail_view, name='participant-detail'),

    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),
    path('recordings/<int:pk>/update/', RecordingUpdateView.as_view(), name='rec-update'),

    path('files/', file_list_view, name='file-list')
]
