from django.db import models


class Recording(models.Model):
    name = models.CharField(max_length=50)

    QUALITY_CHOICES = {
        ('H', 'high'),
        ('M', 'medium'),
        ('L', 'low'),
        ('U', 'n/a')
    }

    quality = models.CharField(choices=QUALITY_CHOICES,
                               max_length=20,
                               default='U')

    CHILD_SPEECH_CHOICES = {
        'L': 'little',
        'LN': 'little to none',
        'M': 'medium',
        'H': 'much',
        'N': 'none',
        'U': 'n/a'
    }

    child_speech = models.CharField(choices=CHILD_SPEECH_CHOICES,
                                    max_length=30,
                                    default='U')

    DIRECTEDNESS_CHOICES = {
        'AA': 'adult>adult',
        'AC': 'adult>child',
        'CC': 'child>child',
        'M': 'mixed',
        'N': 'none',
        'U': 'n/a'
    }

    directedness = models.CharField(choices=DIRECTEDNESS_CHOICES,
                                    max_length=30,
                                    default='U')

    DENE_SPEECH_CHOICES = {
        'L': 'little',
        'M': 'medium',
        'H': 'much',
        'N': 'none',
        'U': 'n/a'
    }

    dene_speech = models.CharField(choices=DENE_SPEECH_CHOICES,
                                   max_length=30,
                                   default='U')

    audio = models.CharField(max_length=100, default='n/a')
    length = models.DurationField(null=True)



