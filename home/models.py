from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile-images/', default='user-placeholder.jpg')
    #function = models.CharField(choices=['Glosser', 'Programmer', 'Manager'])

