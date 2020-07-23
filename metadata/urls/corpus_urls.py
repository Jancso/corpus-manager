from django.urls import path

from metadata.views import corpus_views

urlpatterns = [
    path('corpus/',
         corpus_views.corpus_detail_view,
         name='corpus-detail'),
    path('corpus/update/',
         corpus_views.corpus_update_view,
         name='corpus-update'),
]
