from django.urls import path
from workflow.views.views import (
    workflow_view,
    MonitorImportView
)
from workflow.views.task_views import assigned_task_list_view, \
    open_task_list_view, TaskUpdateView
from workflow.views.rec_views import rec_list_view, rec_detail_view
from workflow.views.forum_views import discussion_list_view, \
    discussion_create_view, discussion_detail_view, CommentUpdateView, \
    DisussionUpdateView

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
    path('recordings/', rec_list_view, name='rec-list'),
    path('recordings/tasks/open', open_task_list_view, name='open-task-list'),
    path('recordings/tasks/assigned',
         assigned_task_list_view,
         name='assigned-task-list'),
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),
    path('tasks/<int:pk>/update/',
         TaskUpdateView.as_view(),
         name='task-update'),
    path('discussions/', discussion_list_view, name='discussion-list'),
    path('discussion/create/', discussion_create_view, name='discussion-create'),
    path('discussion/<int:pk>/', discussion_detail_view, name='discussion-detail'),
    path('discussion/<int:pk>/update/', DisussionUpdateView.as_view(), name='discussion-update'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('monitor/import/', MonitorImportView.as_view(), name='monitor-import')
]
