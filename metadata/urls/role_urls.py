from django.urls import path

from metadata.views import role_views

urlpatterns = [
    path('roles/',
         role_views.role_list_view,
         name='role-list'),
    path('roles/create/',
         role_views.role_create_view,
         name='role-create'),
    path('roles/<int:pk>/update/',
         role_views.role_update_view,
         name='role-update'),
    path('roles/<int:pk>/delete/',
         role_views.role_delete_view,
         name='role-delete'),
    path('roles/import/',
         role_views.role_import_view,
         name='role-import'),
]
