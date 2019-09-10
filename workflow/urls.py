from django.urls import path
from .views import workflow_view, rec_create_view, assignments_list_view

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
    path('rec/create/', rec_create_view, name='rec-create'),
    path('assignments/<str:task>',
         assignments_list_view,
         name='assignments-list')
]
