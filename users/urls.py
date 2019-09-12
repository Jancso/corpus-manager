from django.urls import path
from .views import UserUpdateView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail')
]
