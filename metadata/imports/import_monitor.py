import csv
import re
from io import StringIO
from workflow.models import Task, Assignment
from metadata.models import Recording, Session
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
status_names['complete/in progress'] = Task.STATUS_COMPLETE


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
    'Alexandra': ['alexandra_bosshard'],
    'Alexandra Bosshard': ['alexandra_bosshard'],
    'Allison': ['allison_lemaigre'],
    'Amber': ['amber_fontaine'],
    'Amelie Paulsen': ['amelie_paulsen'],
    'Andrea Lemaigre': ['andrea_lemaigre'],
    'Andrea Lemaigre (Tamara L)': ['andrea_lemaigre', 'tamara_lemaigre'],
    'Andreas Gerster': ['andreas_gerster'],
    'Andreas Gerster(CR)': ['andreas_gerster', 'caroline_remensberger'],
    'Andre Mueller': ['andre_mueller'],
    'Andre Muellet (AP)': ['andre_mueller', 'amelie_paulsen'],
    'Candace Janvier': ['candace_janvier'],
    'Caroline': ['caroline_remensberger'],
    'Caroline Remensberger': ['caroline_remensberger'],
    'Caro Rem (CFo)': ['caroline_remensberger', 'curtis_fontaine'],
    'C/D': ['chastity_sylvestre', 'dawn_herman'],
    'C/D???': ['chastity_sylvestre', 'dawn_herman'],
    'C/D (Allison)': ['chastity_sylvestre', 'dawn_herman', 'allison_lemaigre'],
    'C/D (DCU)': ['chastity_sylvestre', 'dawn_herman', 'dene_cheecham_ulrich'],
    'C/D (HP) (MR)': ['chastity_sylvestre', 'dawn_herman', 'heather_piche', 'mary_ruelling'],
    'C/D MaRue': ['chastity_sylvestre', 'dawn_herman', 'mary_ruelling'],
    'Chastity': ['chastity_sylvestre'],
    'Chastity/Dawn': ['chastity_sylvestre','dawn_herman'],
    'Chastity Sylvestre': ['chastity_sylvestre'],
    'CS/DH': ['chastity_sylvestre', 'dawn_herman'],
    'Curtis': ['curtis_fontaine'],
    'Curtis/Leanne': ['curtis_fontaine', 'leanne_fontaine'],
    'Cynthia': ['cynthia'],
    'Dagmar Jung': ['dagmar_jung'],
    'Dawn/Chastity': ['dawn_herman', 'chastity_sylvestre'],
    'Debora Beuret': ['debora_beuret'],
    'DJ': ['dagmar_jung'],
    'DJ/CS': ['dagmar_jung', 'chastity_sylvestre'],
    'Erika Herman': ['erika_herman'],
    'Farris Lemaigre': ['farris_lemaigre'],
    'FaLemaigre/Trrina Lemaigre': ['farris_lemaigre', 'trina_lemaigre'],
    'Gabrielle/Curtis': ['gabrielle_fontaine', 'curtis_fontaine'],
    'Gabrielle (Curtis) Fontaine': ['gabrielle_fontaine', 'curtis_fontaine'],
    'Gabrielle Fontaine': ['gabrielle_fontaine'],
    'Geneva Moise': ['geneva_moise'],
    'Jeanette': ['jeanette_wiens'],
    'Jeanette Wiens': ['jeanette_wiens'],
    'Jeanette Wiens (CF)': ['jeanette_wiens', 'curtis_fontaine'],
    'Jeanette Wiens (LF)': ['jeanette_wiens', 'leanne_fontaine'],
    'Jeremiah Mercredi': ['jeremiah_mercredi'],
    'Jessica/Dallas': ['jessica_lemaigre', 'dallas'],
    'Jessica Gutiw': ['jessica_gutiw'],
    'Jessica Lemaigre': ['jessica_lemaigre'],
    'JK (Jer (Mandy)': ['jordan_klein', 'jeremiah_mercredi', 'mandy_herman'],
    'JL?': ['jessica_lemaigre'],
    'Jordan Klein': ['jordan_klein'],
    'Jordan Klein (AlL)': ['jordan_klein', 'allison_lemaigre'],
    'JW (Jer/Mandy)': ['jeanette_wiens', 'jeremiah_mercredi', 'mandy_herman'],
    'JW/Jessica Gutiw': ['jeanette_wiens', 'jessica_gutiw'],
    'Leanne': ['leanne_fontaine'],
    'Leanne Fontaine': ['leanne_fontaine'],
    'Mary Roy': ['mary_roy'],
    'Mary Ruelling': ['mary_ruelling'],
    'Melanie Truessel': ['melanie_truessel'],
    'new stud assist FNUNIV': [None],
    'next': [None],
    'not started': [None],
    'Rae Cheecham (MHE)': ['rae_cheecham', 'mandy_herman'],
    'Rae Cheecham/JordanK': ['rae_cheecham', 'jordan_klein'],
    'RM/CS': ['ruben_moegel', 'chastity_sylvestre'],
    'RM (DC)': ['ruben_moegel', 'dene_cheecham_ulrich'],
    'Rolf': ['rolf_hotz'],
    'Rolf Hotz': ['rolf_hotz'],
    'Ruben': ['ruben_moegel'],
    'Ruben (AF)': ['ruben_moegel', 'amber_fontaine'],
    'Ruben Moegel': ['ruben_moegel'],
    'SAP - I think this is actually SOP?': [None],
    'Taylor Fontaine': ['taylor_fontaine'],
    'Taylor Fontaine(Leanne Fontaine)': ['taylor_fontaine', 'leanne_fontaine'],
    'Trina (FL)': ['trina_lemaigre', 'farris_lemaigre'],
    'Trina Lemaigre': ['trina_lemaigre'],
    'Trina Lemaigre (Andrea)': ['trina_lemaigre', 'andrea_lemaigre'],
    'Trina Lemaigre (CF)': ['trina_lemaigre', 'curtis_fontaine'],
    'Trina Lemaigre(EH)': ['trina_lemaigre', 'erika_herman'],
    'TrL/JG': ['trina_lemaigre', 'jessica_gutiw']
}


def _get_session_code(rec_name):
    regex = re.compile(r"deslas-[A-Z]{3,}-\d\d\d\d-\d\d-\d\d(-\d+)?")
    match = regex.search(rec_name)

    if match:
        return match.group()
    else:
        return None


def import_monitor(file):
    Recording.objects.all().delete()
    Task.objects.all().delete()
    Assignment.objects.all().delete()

    file = file.read().decode()

    reader = csv.DictReader(StringIO(file), fieldnames=FIELDNAMES)

    next(reader)

    for row in reader:

        session_name = _get_session_code(row['recording name'])
        try:
            session = Session.objects.get(name=session_name)
        except Session.DoesNotExist:
            print(f'Session {session_name} does not exist!')
            continue

        rec, _ = Recording.objects.update_or_create(
            name=row['recording name'],
            session=session,
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
