from django.urls import path

from metadata.views import corpus_views

urlpatterns = [
    path('corpus/',
         corpus_views.corpus_detail_view,
         name='corpus-detail'),
    path('corpus/<int:pk>/general/update/',
         corpus_views.CorpusGeneralUpdate.as_view(),
         name='corpus-general-update'),
    path('corpus/<int:pk>/location/update/',
         corpus_views.CorpusLocationUpdate.as_view(),
         name='corpus-location-update'),
    path('corpus/<int:pk>/project/update/',
         corpus_views.CorpusProjectUpdate.as_view(),
         name='corpus-project-update'),
    path('corpus/<int:pk>/contact/update/',
         corpus_views.CorpusContactUpdate.as_view(),
         name='corpus-contact-update'),
    path('corpus/<int:pk>/content/update/',
         corpus_views.CorpusContentUpdate.as_view(),
         name='corpus-content-update'),
    path('corpus/<int:pk>/communicationcontext/update/',
         corpus_views.CorpusCommunicationContextUpdate.as_view(),
         name='corpus-communicationcontext-update'),
    path('corpus/<int:pk>/access/update/',
         corpus_views.CorpusAccessUpdate.as_view(),
         name='corpus-access-update'),
]
