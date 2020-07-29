import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from hurry.filesize import size

from django_countries.fields import CountryField


class CommunicationContext(models.Model):

    class Interactivity(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        INTERACTIVE = 'interactive'
        NON_INTERACTIVE = 'non-interactive'
        SEMI_INTERACTIVE = 'semi-interactive'

    interactivity = models.CharField(
        max_length=20, choices=Interactivity.choices, default=Interactivity.UNSPECIFIED)

    class PlanningType(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        SPONTANEOUS = 'spontaneous'
        SEMI_SPONTANEOUS = 'semi-spontaneous'
        PLANNED = 'planned'

    planning_type = models.CharField(
        max_length=20, choices=PlanningType.choices, default=PlanningType.UNSPECIFIED)

    class Involvement(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        ELICITED = 'elicited'
        NON_ELICITED = 'non-elicited'
        NO_OBSERVER = 'no-observer'

    involvement = models.CharField(
        max_length=20, choices=Involvement.choices, default=Involvement.UNSPECIFIED)

    class SocialContext(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        FAMILIY = 'Family'
        PRIVATE = 'Private'
        PUBLIC = 'Public'
        CONTROLLED_ENVIRONMENT = 'Controlled environment'
        PUBLIC_SCHOOL = 'Public (school)'
        COMMUNITY = 'Community'

    social_context = models.CharField(
        max_length=30, choices=SocialContext.choices, default=SocialContext.UNSPECIFIED)

    class EventStructure(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        MONOLOGUE = 'Monologue'
        DIALOGUE = 'Dialogue'
        MULTILOGUE = 'Multilogue'
        NOT_A_NATURAL_FORMAT = 'Not a natural format'
        CONVERSATION = 'Conversation'

    event_structure = models.CharField(
        max_length=30, choices=EventStructure.choices, default=EventStructure.UNSPECIFIED)

    class Channel(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        FACE_TO_FACE = 'Face to Face'
        EXPERIMENTAL_SETTING = 'Experimental setting'
        BROADCASTING = 'Broadcasting'
        TELEPHONE = 'Telephone'
        WIZARD_OF_OZ = 'wizard-of-oz'
        HUMAN_MACHINE_DIALOGUE = 'Human-machine dialogue'
        OTHER = 'Other'

    channel = models.CharField(
        max_length=30, choices=Channel.choices, default=Channel.UNSPECIFIED)


class Location(models.Model):

    class Continent(models.TextChoices):
        UNKNOWN = 'Unknown'
        UNSPECIFIED = 'Unspecified'
        AFRICA = 'Africa'
        ASIA = 'Asia'
        EUROPE = 'Europe'
        AUSTRALIA = 'Australia'
        OCEANIA = 'Oceania'
        NORTH_AMERICA = 'North-America'
        MIDDLE_AMERICA = 'Middle-America'
        SOUTH_AMERICA = 'South-America'

    continent = models.CharField(
        max_length=30,
        choices=Continent.choices,
        default=Continent.UNSPECIFIED)

    country = CountryField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    organisation = models.CharField(max_length=200, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    pid = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)


class Content(models.Model):
    genre = models.CharField(max_length=50, default='None')
    subgenre = models.CharField(max_length=50, null=True, blank=True)
    task = models.CharField(max_length=50, null=True, blank=True)
    modalities = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)

    communication_context = models.OneToOneField(
        CommunicationContext,
        on_delete=models.CASCADE)


class Corpus(models.Model):
    name = models.CharField(max_length=300)

    project = models.OneToOneField(
        Project, on_delete=models.CASCADE)

    location = models.OneToOneField(
        Location, on_delete=models.CASCADE)

    content = models.OneToOneField(
        Content, on_delete=models.CASCADE
    )


class Recording(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)
    session = models.ForeignKey('metadata.Session', on_delete=models.CASCADE)

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
    iso_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, unique=True)


class Participant(models.Model):
    added_by = models.CharField(max_length=50, null=True, blank=True)
    short_name = models.CharField(max_length=10, unique=True)
    anonymized = models.CharField(max_length=3, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    birth_day = models.IntegerField(
        choices=[(i, i) for i in range(1, 32)],
        null=True,
        blank=True)
    birth_month = models.IntegerField(
        choices=[(i, i) for i in range(1, 13)],
        null=True,
        blank=True)
    birth_year = models.IntegerField(
        choices=[(i, i) for i in range(1900, 2100)],
        null=True,
        blank=True)
    age = models.IntegerField(null=True, blank=True)

    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'

    GENDER_CHOICES = [
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male')
    ]

    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10,
                              null=True, blank=True)

    education = models.CharField(max_length=100, null=True, blank=True)

    language_biography = models.CharField(max_length=200, null=True, blank=True)

    description = models.CharField(max_length=200, null=True, blank=True)

    def get_birth_date(self):
        if self.birth_day and self.birth_month and self.birth_year:
            return datetime.date(self.birth_year,
                                 self.birth_month,
                                 self.birth_day)
        else:
            return self.birth_year


class ParticipantLangInfo(models.Model):
    participant = models.ForeignKey('metadata.Participant', on_delete=models.CASCADE)
    language = models.ForeignKey('metadata.Language', on_delete=models.PROTECT)
    main = models.BooleanField()
    first = models.BooleanField()
    second = models.BooleanField()

    class Meta:
        unique_together = ('participant', 'language')


class Session(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    location = models.CharField(max_length=50, null=True, blank=True)
    situation = models.CharField(max_length=200, null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    comments = models.CharField(max_length=200, null=True, blank=True)

    def get_target_child(self):
        tcs = self.sessionparticipant_set.filter(roles__name__exact='child')
        if tcs:
            return tcs[0].participant
        else:
            return None

    def get_target_child_age(self):
        tc = self.get_target_child()
        if tc:
            birth_date = tc.get_birth_date()
            if birth_date and self.date:
                delta = self.date - relativedelta(
                    years=birth_date.year,
                    days=birth_date.day,
                    months=birth_date.month)
                return f'{delta.year};{delta.month}.{delta.day}'

        return None


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)


class SessionParticipant(models.Model):
    session = models.ForeignKey('metadata.Session', on_delete=models.CASCADE)
    participant = models.ForeignKey('metadata.Participant', on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, through='metadata.SessionParticipantRole')

    class Meta:
        unique_together = ('session', 'participant')


class SessionParticipantRole(models.Model):
    session_participant = models.ForeignKey('metadata.SessionParticipant', on_delete=models.CASCADE)
    role = models.ForeignKey('metadata.Role', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('session_participant', 'role')


class File(models.Model):
    name = models.CharField(max_length=50)

    recording = models.ForeignKey('metadata.Recording', on_delete=models.CASCADE)

    TYPE_AUDIO = 'audio'
    TYPE_VIDEO = 'video'

    TYPE_CHOICES = [
        (TYPE_AUDIO, TYPE_AUDIO),
        (TYPE_VIDEO, TYPE_VIDEO)
    ]

    type = models.CharField(choices=TYPE_CHOICES, max_length=5)

    FORMAT_MP4 = 'mp4'
    FORMAT_MTS = 'mts'
    FORMAT_WAV = 'wav'
    FORMAT_MOV = 'mov'

    FORMAT_CHOICES = [
        (FORMAT_MOV, FORMAT_MOV),
        (FORMAT_MP4, FORMAT_MP4),
        (FORMAT_MTS, FORMAT_MTS),
        (FORMAT_WAV, FORMAT_WAV)
    ]

    format = models.CharField(choices=FORMAT_CHOICES, max_length=3)

    duration = models.DurationField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def get_human_readable_size(self):
        return size(self.size)
