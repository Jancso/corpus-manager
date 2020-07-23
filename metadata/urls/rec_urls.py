from django.urls import path

from metadata.views import rec_views

urlpatterns = [
    path('recordings/',
         rec_views.rec_list_view,
         name='rec-list'),
    path('recordings/<int:pk>/',
         rec_views.rec_detail_view,
         name='rec-detail'),
    path('recordings/<int:pk>/delete/',
         rec_views.rec_delete_view,
         name='rec-delete'),
    path('recordings/<int:pk>/update/',
         rec_views.RecordingUpdateView.as_view(),
         name='rec-update'),
    path('recordings/create/',
         rec_views.rec_create_view,
         name='rec-create'),

]
