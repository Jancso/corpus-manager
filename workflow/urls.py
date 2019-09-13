from django.urls import path
from .views import (
    workflow_view,
    rec_create_view,
    rec_detail_view,
    RecordingUpdateView,
    TaskUpdateView,
    rec_delete_view
)

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
    path('rec/create/', rec_create_view, name='rec-create'),
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),
    path('recordings/<int:pk>/update/',
         RecordingUpdateView.as_view(),
         name='rec-update'),
    path('tasks/<int:pk>/update/',
         TaskUpdateView.as_view(),
         name='task-update'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),

]
