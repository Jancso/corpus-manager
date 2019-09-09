from django.urls import path
from .views import workflow_view

app_name = 'workflow'

urlpatterns = [
    path('', workflow_view, name='workflow'),
]
