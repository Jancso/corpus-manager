from django.db import models


class Recording(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)
    session = models.ForeignKey('metadata.Session', on_delete=models.CASCADE, null=True)

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


class Language(models.Model):
    iso_code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)


class Participant(models.Model):
    added_by = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50)
    birth_date = models.CharField(max_length=50)

    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'

    GENDER_CHOICES = [
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male')
    ]

    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10,
                              null=True)

    education = models.CharField(max_length=100)

    language_biography = models.CharField(max_length=200)
    languages = models.ManyToManyField('metadata.Language', through='ParticipantLangInfo')


class ParticipantLangInfo(models.Model):
    participant = models.ForeignKey('metadata.Participant', on_delete=models.CASCADE)
    language = models.ForeignKey('metadata.Language', on_delete=models.CASCADE)
    main = models.BooleanField()
    first = models.BooleanField()
    second = models.BooleanField()


class Session(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    location = models.CharField(max_length=50)
    duration = models.DurationField()
    situation = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)
    participants = models.ManyToManyField('metadata.Participant')


class File(models.Model):
    name = models.CharField(max_length=50)

    recording = models.ForeignKey('metadata.Recording', on_delete=models.CASCADE)

    TYPE_AUDIO = 'A'
    TYPE_VIDEO = 'V'

    TYPE_CHOICES = [
        (TYPE_AUDIO, 'audio'),
        (TYPE_VIDEO, 'video')
    ]

    type = models.CharField(choices=TYPE_CHOICES, max_length=5)

    FORMAT_MP4 = 'mp4'
    FORMAT_MTS = 'mts'
    FORMAT_WAV = 'wav'
    FORMAT_MOV = 'mov'

    FORMAT_CHOICES = [
        (FORMAT_MOV, 'MOV'),
        (FORMAT_MP4, 'MP4'),
        (FORMAT_MTS, 'MTS'),
        (FORMAT_WAV, 'WAV')
    ]

    format = models.CharField(choices=FORMAT_CHOICES, max_length=3)

    duration = models.DurationField()
    bytes = models.IntegerField()
    location = models.CharField(max_length=50)