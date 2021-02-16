from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='profile-images/',
                              default='user-placeholder.jpg',
                              blank=True)

    JOB_FUNCTION_CHOICES = [
        ('GL', 'Glosser'),
        ('MA', 'Manager'),
        ('PR', 'Programmer'),
    ]

    job_function = models.CharField(choices=JOB_FUNCTION_CHOICES,
                                    default='GL',
                                    max_length=30)
