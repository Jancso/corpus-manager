import csv
from io import StringIO
from .models import Task, Assignment
from metadata.models import Recording
from datetime import timedelta, datetime
from users.models import User, UserProfile

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

status_names = {v: k for k, v in Task.STATUS_CHOICES}
status_names['completed'] = Task.STATUS_COMPLETE
status_names[''] = Task.STATUS_NOT_STARTED


def to_timedelta(duration):
    if duration:
        if duration in ['0', '???', 'invalid']:
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


people_dict = {
    '': [None],
    '???': [None],
    'Alexandra': ['alexandra'],
    'Alexandra Bosshard': ['alexandra'],
    'Allison': ['allison'],
    'Amber': ['amber'],
    'Amelie Paulsen': ['amelie'],
    'Andrea Lemaigre': ['andrea'],
    'Andrea Lemaigre (Tamara L)': ['andrea', 'tamara'],
    'Andreas Gerster': ['andreas'],
    'Andreas Gerster(CR)': ['andreas'],
    'Andre Mueller': ['andre'],
    'Candace Janvier': ['candace'],
    'Caroline': ['caroline'],
    'Caroline Remensberger': ['caroline'],
    'Caro Rem (CFo)': ['caroline'],
    'C/D': [None],
    'C/D???': [None],
    'C/D (Allison)': [None, 'allison'],
    'C/D (DCU)': [None, None],
    'C/D (HP) (MR)': [None, None, None],
    'C/D MaRue': [None, None],
    'Chastity': ['chastity'],
    'Chastity/Dawn': ['chastity','dawn'],
    'Chastity Sylvestre': ['chastity'],
    'CS/DH': [None, None],
    'Curtis': ['curtis'],
    'Curtis/Leanne': ['curtis', 'leanne'],
    'Cynthia': ['cynthia'],
    'Dagmar Jung': ['dagmar'],
    'Dawn/Chastity': ['dawn', 'chastity'],
    'Debora Beuret': ['debora'],
    'DJ': ['dagmar'],
    'DJ/CS': ['dagmar'],
    'Erika Herman': ['erika'],
    'Farris Lemaigre': ['farris'],
    'Gabrielle/Curtis': ['gabrielle', 'curtis'],
    'Gabrielle (Curtis) Fontaine': ['gabrielle', 'curtis'],
    'Gabrielle Fontaine': ['gabrielle'],
    'Geneva Moise': ['geneva'],
    'Jeanette': ['jeanette'],
    'Jeanette Wiens': ['jeanette'],
    'Jeanette Wiens (CF)': ['jeanette'],
    'Jeanette Wiens (LF)': ['jeanette'],
    'Jeremiah Mercredi': ['jeremia'],
    'Jessica/Dallas': [None, 'dallas'],
    'Jessica Gutiw': ['gutiw'],
    'Jessica Lemaigre': ['lemaigre'],
    'JK (Jer (Mandy)': [None, 'jer', 'mandy'],
    'JL?': [None],
    'Jordan Klein': ['jordan'],
    'Jordan Klein (AlL)': ['jordan', None],
    'JW (Jer/Mandy)': ['jeanette', 'jer', 'mandy'],
    'JW/Jessica Gutiw': ['jeanette', 'gutiw'],
    'Leanne': ['leanne'],
    'Leanne Fontaine': ['leanne'],
    'Mary Roy': ['roy'],
    'Mary Ruelling': ['ruelling'],
    'Melanie Truessel': ['melanie'],
    'new stud assist FNUNIV': [None],
    'not started': [None],
    'Rae Cheecham (MHE)': ['rae'],
    'Rae Cheecham/JordanK': ['rae', 'jordan'],
    'RM/CS': [None, None],
    'RM (DC)': [None, None],
    'Rolf': ['rolf'],
    'Rolf Hotz': ['rolf'],
    'Ruben': ['ruben'],
    'Ruben (AF)': ['ruben'],
    'Ruben Moegel': ['ruben'],
    'SAP - I think this is actually SOP?': [None],
    'Taylor Fontaine': ['taylor'],
    'Trina (FL)': ['trina'],
    'Trina Lemaigre': ['trina'],
    'Trina Lemaigre (Andrea)': ['trina', 'andrea'],
    'Trina Lemaigre (CF)': ['trina', None],
    'Trina Lemaigre(EH)': ['trina', None],
}


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
                status = status_names[row['status segmentation']]
                start = to_date(row['start segmentation'])
                end = to_date(row['end segmentation'])
                people = people_dict[row['person segmentation']]
            elif task_name_i == Task.TRANSCRIPTION:
                status = status_names[row['status transcription/translation']]
                start = to_date(row['start transcription/translation'])
                end = to_date(row['end transcription/translation'])
                people = people_dict[row['person transcription/translation']]
            else:
                status = status_names[row['status glossing']]
                start = to_date(row['start glossing'])
                end = to_date(row['end glossing'])
                people = people_dict[row['person glossing']]

            task, _ = Task.objects.update_or_create(
                recording=rec,
                name=task_name_i,
                defaults={
                    'status': status,
                    'start': start,
                    'end': end
                }
            )

            for person_name in people:
                if person_name:

                    user, _ = User.objects.update_or_create(
                        username=person_name,
                        email='',
                        defaults={
                            'first_name': person_name.title()
                        }
                    )

                    user.set_password('matterhorn')
                    user.save()

                    UserProfile.objects.update_or_create(
                        user=user
                    )

                    Assignment.objects.update_or_create(
                        task=task,
                        person=user
                    )
