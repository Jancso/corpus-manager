from django.urls import path
from .views import UserUpdateView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]
