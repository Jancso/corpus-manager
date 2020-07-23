from django.urls import path

from metadata.views import session_views

urlpatterns = [
    path('sessions/',
         session_views.session_list_view,
         name='session-list'),
    path('sessions/<int:pk>/',
         session_views.session_detail_view,
         name='session-detail'),
    path('sessions/<int:pk>/update/',
         session_views.SessionUpdateView.as_view(),
         name='session-update'),
    path('sessions/<int:pk>/delete/',
         session_views.session_delete_view,
         name='session-delete'),
    path('sessions/<int:pk>/participants/create/',
         session_views.session_participants_create_view,
         name='session-participants-create'),
    path('sessions/<int:spk>/participants/<int:ppk>/delete/',
         session_views.session_participant_delete_view,
         name='session-participant-delete'),
    path('sessions/<int:spk>/participants/<int:ppk>/update/',
         session_views.SessionParticipantUpdateView.as_view(),
         name='session-participant-update'),
    path('sessions/export/csv/',
         session_views.session_csv_export_view,
         name='session-csv-export'),
]
