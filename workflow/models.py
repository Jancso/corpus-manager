from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    recording = models.ForeignKey('metadata.Recording', on_delete=models.CASCADE)

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
    recordings = models.ManyToManyField('metadata.Recording')


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    description = models.TextField()
