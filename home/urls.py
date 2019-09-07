from django.urls import path
from .views import home_detail_view

app_name = 'home'

urlpatterns = [
    path('', home_detail_view, name='home-detail')
]