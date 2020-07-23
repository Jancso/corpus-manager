from django.urls import path, include

from metadata.views import general_views

app_name = 'metadata'

urlpatterns = [
    path('',
         general_views.metadata_view,
         name='metadata-view'),

    path('', include('metadata.urls.session_urls')),
    path('', include('metadata.urls.participant_urls')),
    path('', include('metadata.urls.role_urls')),
    path('', include('metadata.urls.language_urls')),
    path('', include('metadata.urls.rec_urls')),
    path('', include('metadata.urls.file_urls')),

    path('import/',
         general_views.MetadataImportView.as_view(),
         name='metadata-import')
]
