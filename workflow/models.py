from django.db import models
from django.contrib.auth.models import User


class Recording(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)

    QUALITY_HIGH = 'H'
    QUALITY_MEDIUM = 'M'
    QUALITY_LOW = 'L'
    QUALITY_NA = 'U'

    QUALITY_CHOICES = [
        (QUALITY_HIGH, 'high'),
        (QUALITY_MEDIUM, 'medium'),
        (QUALITY_LOW, 'low'),
        (QUALITY_NA, 'n/a')
    ]

    quality = models.CharField(choices=QUALITY_CHOICES,
                               max_length=20,
                               default=QUALITY_NA)

    CHILD_SPEECH_LITTLE = 'L'
    CHILD_SPEECH_LITTLE_TO_NONE = 'LN'
    CHILD_SPEECH_MEDIUM = 'M'
    CHILD_SPEECH_HIGH = 'H'
    CHILD_SPEECH_NONE = 'N'
    CHILD_SPEECH_NA = 'U'

    CHILD_SPEECH_CHOICES = [
        (CHILD_SPEECH_LITTLE, 'little'),
        (CHILD_SPEECH_LITTLE_TO_NONE, 'little to none'),
        (CHILD_SPEECH_MEDIUM, 'medium'),
        (CHILD_SPEECH_HIGH, 'much'),
        (CHILD_SPEECH_NONE, 'none'),
        (CHILD_SPEECH_NA, 'n/a')
    ]

    child_speech = models.CharField(choices=CHILD_SPEECH_CHOICES,
                                    max_length=30,
                                    default=CHILD_SPEECH_NA)

    DIRECTEDNESS_ADULT_ADULT = 'AA'
    DIRECTEDNESS_ADULT_CHILD = 'AC'
    DIRECTEDNESS_CHILD_CHILD = 'CC'
    DIRECTEDNESS_MIXED = 'M'
    DIRECTEDNESS_NONE = 'N'
    DIRECTEDNESS_NA = 'U'

    DIRECTEDNESS_CHOICES = [
        (DIRECTEDNESS_ADULT_ADULT, 'adult>adult'),
        (DIRECTEDNESS_ADULT_CHILD, 'adult>child'),
        (DIRECTEDNESS_CHILD_CHILD, 'child>child'),
        (DIRECTEDNESS_MIXED, 'mixed'),
        (DIRECTEDNESS_NONE, 'none'),
        (DIRECTEDNESS_NA, 'n/a')
    ]

    directedness = models.CharField(choices=DIRECTEDNESS_CHOICES,
                                    max_length=30,
                                    default=DIRECTEDNESS_NA)

    DENE_SPEECH_LITTLE = 'L'
    DENE_SPEECH_MEDIUM = 'M'
    DENE_SPEECH_HIGH = 'H'
    DENE_SPEECH_NONE = 'N'
    DENE_SPEECH_NA = 'U'

    DENE_SPEECH_CHOICES = [
        (DENE_SPEECH_LITTLE, 'little'),
        (DENE_SPEECH_MEDIUM, 'medium'),
        (DENE_SPEECH_HIGH, 'much'),
        (DENE_SPEECH_NONE, 'none'),
        (DENE_SPEECH_NA, 'n/a')
    ]

    dene_speech = models.CharField(choices=DENE_SPEECH_CHOICES,
                                   max_length=30,
                                   default=DENE_SPEECH_NA)

    audio = models.CharField(max_length=100, null=True, blank=True)
    length = models.DurationField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


class Task(models.Model):

    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)

    SEGMENTATION = 'segmentation'
    TRANSCRIPTION = 'transcription'
    TRANSCRIPTION_CHECK = 'transcription check'
    GLOSSING = 'glossing'
    GLOSSING_CHECK = 'glossing check'

    NAME_CHOICES = [
        (SEGMENTATION, 'segmentation'),
        (TRANSCRIPTION, 'transcription/translation'),
        #(TRANSCRIPTION_CHECK, 'check transcription/translation'),
        (GLOSSING, 'glossing'),
        #(GLOSSING_CHECK, 'check glossing'),
    ]

    name = models.CharField(choices=NAME_CHOICES,
                            max_length=50)

    STATUS_NOT_STARTED = 'NOT-STARTED'
    STATUS_BARRED = 'BARRED'
    STATUS_DEFERRED = 'DEFERRED'
    STATUS_RESERVED = 'RESERVED'
    STATUS_IN_PROGRESS = 'IN PROGRESS'
    STATUS_CHECKED = 'CHECKED'
    STATUS_INCOMPLETE = 'INCOMPLETE'
    STATUS_COMPLETE = 'COMPLETE'
    STATUS_NO_MEDIA = 'NO MEDIA'
    STATUS_PROBLEMS = 'PROBLEMS'
    STATUS_UNCLEAR = 'UNCLEAR'

    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, 'not started'),
        (STATUS_BARRED, 'barred'),
        (STATUS_DEFERRED, 'defer'),
        (STATUS_RESERVED, 'reserved for'),
        (STATUS_IN_PROGRESS, 'in progress'),
        (STATUS_CHECKED, 'CHECK'),
        (STATUS_INCOMPLETE, 'incomplete'),
        (STATUS_COMPLETE, 'complete'),
        (STATUS_NO_MEDIA, 'no media'),
        (STATUS_PROBLEMS, 'problems'),
        (STATUS_UNCLEAR, 'UNCLEAR')
    ]

    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=30,
                              default=STATUS_NOT_STARTED)

    start = models.DateField(null=True, blank=True)

    end = models.DateField(null=True, blank=True)

    finished_task_statuses = [STATUS_INCOMPLETE, STATUS_COMPLETE]

    def is_finished(self):
        return self.status in self.finished_task_statuses

    def is_free(self):
        return self.status == self.STATUS_NOT_STARTED

    class Meta:
        unique_together = ('recording', 'name')


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'person')


class Discussion(models.Model):
    title = models.CharField(max_length=50, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    description = models.TextField()
    recordings = models.ManyToManyField(Recording)


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    description = models.TextField()
