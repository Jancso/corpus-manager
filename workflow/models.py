from django.db import models


class Recording(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)

    QUALITY_CHOICES = [
        ('H', 'high'),
        ('M', 'medium'),
        ('L', 'low'),
        ('U', 'n/a')
    ]

    quality = models.CharField(choices=QUALITY_CHOICES,
                               max_length=20,
                               default='U')

    CHILD_SPEECH_CHOICES = [
        ('L', 'little'),
        ('LN', 'little to none'),
        ('M', 'medium'),
        ('H', 'much'),
        ('N', 'none'),
        ('U', 'n/a')
    ]

    child_speech = models.CharField(choices=CHILD_SPEECH_CHOICES,
                                    max_length=30,
                                    default='U')

    DIRECTEDNESS_CHOICES = [
        ('AA', 'adult>adult'),
        ('AC', 'adult>child'),
        ('CC', 'child>child'),
        ('M', 'mixed'),
        ('N', 'none'),
        ('U', 'n/a')
    ]

    directedness = models.CharField(choices=DIRECTEDNESS_CHOICES,
                                    max_length=30,
                                    default='U')

    DENE_SPEECH_CHOICES = [
        ('L', 'little'),
        ('M', 'medium'),
        ('H', 'much'),
        ('N', 'none'),
        ('U', 'n/a')
    ]

    dene_speech = models.CharField(choices=DENE_SPEECH_CHOICES,
                                   max_length=30,
                                   default='U')

    audio = models.CharField(max_length=100, null=True, blank=True)
    length = models.DurationField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


class Task(models.Model):

    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)

    NAME_CHOICES = [
        ('S', 'segmentation'),
        ('T', 'transcription/translation'),
        ('CT', 'check transcription/translation'),
        ('G', 'glossing'),
        ('CG', 'check glossing'),
    ]

    name = models.CharField(choices=NAME_CHOICES,
                            max_length=50)

    STATUS_CHOICES = [
        ('BARRED', 'barred'),
        ('CHECKED', 'checked'),
        ('COMPLETED', 'completed'),
        ('DEFERRED', 'defered'),
        ('INCOMPLETE', 'incomplete'),
        ('IN-PROGRESS', 'in progress'),
        ('NOT-STARTED', 'not started'),
        ('RESERVED', 'reserved for'),
    ]

    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=30,
                              default='NOT-STARTED')

    end = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('recording', 'name')


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.CharField(unique=True, max_length=50)
    start = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'person')
