from django.urls import path

from metadata.views import rec_create_view, rec_delete_view, \
    RecordingUpdateView, metadata_view, rec_list_view

app_name = 'metadata'

urlpatterns = [
    path('', metadata_view, name='metadata-view'),

    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/create/', rec_create_view, name='rec-create'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),
    path('recordings/<int:pk>/update/', RecordingUpdateView.as_view(), name='rec-update'),
]
