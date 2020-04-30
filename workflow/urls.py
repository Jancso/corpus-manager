from django.urls import path
from workflow.views.views import workflow_view
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
    path('recordings/<int:pk>/', rec_detail_view, name='rec-detail'),

    path('tasks/open', open_task_list_view, name='open-task-list'),
    path('tasks/assigned', assigned_task_list_view, name='assigned-task-list'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),

    path('discussions/', discussion_list_view, name='discussion-list'),
    path('discussions/create/', discussion_create_view, name='discussion-create'),
    path('discussions/<int:pk>/', discussion_detail_view, name='discussion-detail'),
    path('discussions/<int:pk>/update/', DisussionUpdateView.as_view(), name='discussion-update'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
]
