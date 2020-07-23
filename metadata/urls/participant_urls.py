from django.urls import path

from metadata.views import participant_views


urlpatterns = [
    path('participants/',
         participant_views.participant_list_view,
         name='participant-list'),
    path('participants/create/',
         participant_views.ParticipantCreateView.as_view(),
         name='participant-create'),
    path('participants/<int:pk>/',
         participant_views.participant_detail_view,
         name='participant-detail'),
    path('participants/<int:pk>/update/',
         participant_views.ParticipantUpdateView.as_view(),
         name='participant-update'),
    path('participants/<int:pk>/delete/',
         participant_views.participant_delete_view,
         name='participant-delete'),
    path('participants/<int:pk>/languages/create/',
         participant_views.ParticipantLangInfoCreateView.as_view(),
         name='participant-lang-create'),
    path('participants/<int:ppk>/languages/<int:lpk>/delete/',
         participant_views.participant_language_delete_view,
         name='participant-lang-delete'),
    path('participants/<int:ppk>/languages/<int:lpk>/update/',
         participant_views.ParticipantLangUpdateView.as_view(),
         name='participant-lang-update'),
    path('participants/export/csv/',
         participant_views.participant_csv_export_view,
         name='participant-csv-export'),
]
