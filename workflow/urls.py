from django.urls import path
from .views import (
    workflow_view,
    rec_create_view,
    rec_detail_view,
    RecordingUpdateView,
    TaskUpdateView,
    rec_delete_view,
    MonitorImportView,
    rec_list_view,
    open_task_list_view,
    assigned_task_list_view,
    discussion_list_view,
    discussion_create_view,
    discussion_detail_view,
    DisussionUpdateView,
    CommentUpdateView
)

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
    path('rec/create/', rec_create_view, name='rec-create'),
    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/tasks/open', open_task_list_view, name='open-task-list'),
    path('recordings/tasks/assigned',
         assigned_task_list_view,
         name='assigned-task-list'),
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),
    path('recordings/<int:pk>/update/',
         RecordingUpdateView.as_view(),
         name='rec-update'),
    path('tasks/<int:pk>/update/',
         TaskUpdateView.as_view(),
         name='task-update'),
    path('recordings/<int:pk>/delete/', rec_delete_view, name='rec-delete'),
    path('discussions/', discussion_list_view, name='discussion-list'),
    path('discussion/create/', discussion_create_view, name='discussion-create'),
    path('discussion/<int:pk>/', discussion_detail_view, name='discussion-detail'),
    path('discussion/<int:pk>/update/', DisussionUpdateView.as_view(), name='discussion-update'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('monitor/import/', MonitorImportView.as_view(), name='monitor-import')
]
