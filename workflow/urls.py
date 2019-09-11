from django.urls import path
from .views import (
    workflow_view,
    rec_create_view,
    rec_detail_view,
    RecordingUpdateView)

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
    path('rec/create/', rec_create_view, name='rec-create'),
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),
    path('recordings/<int:pk>/update/',
         RecordingUpdateView.as_view(),
         name='rec-update')
]
