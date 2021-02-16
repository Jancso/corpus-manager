from django.urls import path

from metadata.views import file_views

urlpatterns = [
    path('files/',
         file_views.file_list_view,
         name='file-list'),
    path('files/create/',
         file_views.FileCreateView.as_view(),
         name='file-create'),
]
