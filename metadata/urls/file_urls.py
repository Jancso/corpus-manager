from django.urls import path

from metadata.views import file_views

urlpatterns = [
    path('files/',
         file_views.file_list_view,
         name='file-list'),
    path('files/create/',
         file_views.FileCreateView.as_view(),
         name='file-create'),
    path('files/<int:pk>/',
         file_views.file_delete_view,
         name='file-delete'),
    path('files/<int:pk>/update/',
         file_views.FileUpdateView.as_view(),
         name='file-update'),
]
