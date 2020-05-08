from django.urls import path
from users.views.users_views import UserUpdateView, UserDetailView, UserListView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list')
]
