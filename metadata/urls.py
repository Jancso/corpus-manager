from django.urls import path

from metadata.views.rec_views import rec_delete_view, \
    RecordingUpdateView, rec_list_view, rec_create_view, rec_detail_view
from metadata.views.views import metadata_view, MetadataImportView
from metadata.views.role_views import role_import_view, role_list_view, role_create_view, role_delete_view, role_update_view
from metadata.views.session_views import \
    session_list_view, session_detail_view, SessionUpdateView, \
    session_delete_view, session_participants_create_view, \
    session_participant_delete_view, session_csv_export_view, \
    SessionParticipantUpdateView
from metadata.views.file_views import file_list_view
from metadata.views.participant_views import \
    participant_list_view, ParticipantCreateView, participant_detail_view, \
    ParticipantUpdateView, participant_delete_view, ParticipantLangInfoCreateView, participant_language_delete_view, ParticipantLangUpdateView, participant_csv_export_view
from metadata.views.language_views import language_list_view, language_import_view, language_create_view

app_name = 'metadata'

urlpatterns = [
    path('', metadata_view, name='metadata-view'),

    path('languages/', language_list_view, name='language-list'),
    path('languages/create/', language_create_view, name='language-create'),
    path('languages/import/', language_import_view, name='language-import'),

    path('roles/', role_list_view, name='role-list'),
    path('roles/create/', role_create_view, name='role-create'),
    path('roles/<int:pk>/update/', role_update_view, name='role-update'),
    path('roles/<int:pk>/delete/', role_delete_view, name='role-delete'),
    path('roles/import/', role_import_view, name='role-import'),

    path('sessions/', session_list_view, name='session-list'),
    path('sessions/<int:pk>/', session_detail_view, name='session-detail'),
    path('sessions/<int:pk>/update/', SessionUpdateView.as_view(), name='session-update'),
    path('sessions/<int:pk>/delete/', session_delete_view, name='session-delete'),
    path('sessions/<int:pk>/participants/create/', session_participants_create_view, name='session-participants-create'),
    path('sessions/<int:spk>/participants/<int:ppk>/delete/', session_participant_delete_view, name='session-participant-delete'),
    path('sessions/<int:spk>/participants/<int:ppk>/update/',
         SessionParticipantUpdateView.as_view(),
         name='session-participant-update'),
    path('sessions/export/csv/', session_csv_export_view, name='session-csv-export'),

    path('participants/', participant_list_view, name='participant-list'),
    path('participants/create/', ParticipantCreateView.as_view(), name='participant-create'),
    path('participants/<int:pk>/', participant_detail_view, name='participant-detail'),
    path('participants/<int:pk>/update/', ParticipantUpdateView.as_view(), name='participant-update'),
    path('participants/<int:pk>/delete/', participant_delete_view, name='participant-delete'),
    path('participants/<int:pk>/languages/create/', ParticipantLangInfoCreateView.as_view(), name='participant-lang-create'),
    path('participants/<int:ppk>/languages/<int:lpk>/delete/', participant_language_delete_view , name='participant-lang-delete'),
    path('participants/<int:ppk>/languages/<int:lpk>/update/', ParticipantLangUpdateView.as_view(), name='participant-lang-update'),
    path('participants/export/csv/', participant_csv_export_view, name='participant-csv-export'),

    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),
    path('recordings/<int:pk>/update/', RecordingUpdateView.as_view(), name='rec-update'),
    path('recordings/create/', rec_create_view, name='rec-create'),

    path('files/', file_list_view, name='file-list'),

    path('import/', MetadataImportView.as_view(), name='metadata-import')
]
