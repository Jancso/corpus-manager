from django.urls import path
from .views import home_detail_view, settings_detail_view

app_name = 'home'

urlpatterns = [
    path('', home_detail_view, name='home-detail'),
    path('settings/', settings_detail_view, name='settings-detail'),
]