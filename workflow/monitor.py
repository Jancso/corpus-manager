import csv
from io import StringIO
from .models import Recording, Task
from datetime import timedelta, datetime

FIELDNAMES = [
    'recording name',
    'quality',
    'child speech',
    'directedness',
    'Dene',
    'audio',
    'length',
    'status segmentation',
    'person segmentation',
    'start segmentation',
    'end segmentation',
    'status transcription/translation',
    'person transcription/translation',
    'start transcription/translation',
    'end transcription/translation',
    'status check transcription/translation',
    'person check transcription/translation',
    'start check transcription/translation',
    'end check transcription/translation',
    'status glossing',
    'person glossing',
    'start glossing',
    'end glossing',
    'status check glossing',
    'person check glossing',
    'start check glossing',
    'end check glossing',
    'notes'
]

quality_names = {v: k for k, v in Recording.QUALITY_CHOICES}
quality_names[''] = Recording.QUALITY_NA
quality_names['little'] = Recording.QUALITY_LOW

child_speech = {v: k for k, v in Recording.CHILD_SPEECH_CHOICES}
child_speech[''] = Recording.CHILD_SPEECH_NA
child_speech['low'] = Recording.CHILD_SPEECH_LITTLE
child_speech['meidum'] = Recording.CHILD_SPEECH_MEDIUM

directedness = {v: k for k, v in Recording.DIRECTEDNESS_CHOICES}
directedness[''] = Recording.DIRECTEDNESS_NA

dene = {v: k for k, v in Recording.DENE_SPEECH_CHOICES}
dene[''] = Recording.DENE_SPEECH_NA
dene['much '] = Recording.DENE_SPEECH_HIGH

status = {v: k for k, v in Task.NAME_CHOICES}
status['completed'] = Task.STATUS_COMPLETE
status[''] = Task.STATUS_NOT_STARTED


def to_timedelta(duration):
    if duration:
        if duration == '0':
            return None
        hours, minutes, seconds = duration.split(':')
        timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    else:
        return None


def to_date(date):
    if date:
        if date in ['?', '???', '-', 'mpg was too large encoding']:
            return None

        if date == '2018-03-35':
            return datetime.strptime('31.03.18', "%d.%m.%y")

        if date == '08.08.209':
            return datetime.strptime('08.08.19', "%d.%m.%y")

        for fmt in ["%d.%m.%y", "%d.%m.%Y", '%Y-%m-%d']:
            try:
                date = datetime.strptime(date, fmt)
            except:
                pass
            else:
                return date

        print(date)

    return None


def import_(file):
    file = file.read().decode()

    reader = csv.DictReader(StringIO(file), fieldnames=FIELDNAMES)

    next(reader)

    for row in reader:

        rec, _ = Recording.objects.update_or_create(
            name=row['recording name'],
            defaults={
                'quality': quality_names[row['quality']],
                'child_speech': child_speech[row['child speech']],
                'directedness': directedness[row['directedness']],
                'dene_speech': dene[row['Dene']],
                'audio': row['audio'] if row['audio'] else None,
                'length': to_timedelta(row['length']),
                'notes': row['notes'] if row['notes'] else None
            }
        )

        for task_name_i, _ in Task.NAME_CHOICES:

            if task_name_i == Task.SEGMENTATION:
                status = row['status segmentation']
                start = to_date(row['start segmentation'])
                end = to_date(row['end segmentation'])
            elif task_name_i == Task.TRANSCRIPTION:
                status = row['status transcription/translation']
                start = to_date(row['start transcription/translation'])
                end = to_date(row['end transcription/translation'])
            else:
                status = row['status glossing']
                start = to_date(row['start glossing'])
                end = to_date(row['end glossing'])

            task, _ = Task.objects.update_or_create(
                recording=rec,
                name=task_name_i,
                defaults={
                    'status': status,
                    'start': start,
                    'end': end
                }
            )