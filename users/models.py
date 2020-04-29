from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
