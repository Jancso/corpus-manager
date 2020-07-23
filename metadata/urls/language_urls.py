from django.urls import path

from metadata.views import language_views

urlpatterns = [
    path('languages/',
         language_views.language_list_view,
         name='language-list'),
    path('languages/create/',
         language_views.language_create_view,
         name='language-create'),
    path('languages/<int:pk>/update/',
         language_views.language_update_view,
         name='language-update'),
    path('languages/<int:pk>/delete/',
         language_views.language_delete_view,
         name='language-delete'),
    path('languages/import/',
         language_views.language_import_view,
         name='language-import'),

]
