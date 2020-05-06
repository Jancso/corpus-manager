from io import StringIO

from metadata.models import Participant, ParticipantLangInfo, Language
import csv
import re

from metadata.util.generate_random_code import generate_random_code


def import_participants(file):
    Participant.objects.all().delete()

    file = file.read().decode()
    reader = csv.DictReader(StringIO(file))

    participants = set()

    for row in reader:

        if row['Short name'] in participants:
            print(row['Short name'], ' is used twice!')
            continue

        row = dict(row)

        # make empty fields None
        for field in row:
            if row[field] == '':
                row[field] = None
            else:
                if field == 'Age':
                    row[field] = int(row[field])

        birth_day = None
        birth_month = None
        birth_year = None
        if row['Birth date']:
            match = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', row['Birth date'])
            if match:
                birth_day = match.group(3)
                birth_month = match.group(2)
                birth_year = match.group(1)
            else:
                match = re.fullmatch(r'(\d{4})', row['Birth date'])
                if match:
                    birth_year = match.group()

        participant = Participant.objects.create(
            added_by=row['Added by'],
            short_name=row['Short name'],
            anonymized=generate_random_code(),
            full_name=row['Full name'],
            birth_day=birth_day,
            birth_month=birth_month,
            birth_year=birth_year,
            age=row['Age'],
            gender=row['Gender'],
            education=row['Education'],
            language_biography=row['Language biography'],
            description=row['Description']
        )

        participants.add(row['Short name'])

        langs = {}

        for field in ['First languages', 'Second languages', 'Main language']:
            if row[field] is not None:
                for lang in row[field].split('/'):
                    if lang in langs:
                        part_lang_info = langs[lang]
                    else:
                        language = Language.objects.get(name=lang)
                        part_lang_info = ParticipantLangInfo(
                            participant=participant,
                            language=language,
                            main=False,
                            first=False,
                            second=False)
                        langs[lang] = part_lang_info

                    if field == 'First languages':
                        part_lang_info.first = True
                    elif field == 'Second languages':
                        part_lang_info.second = True
                    elif field == 'Main language':
                        part_lang_info.main = True

        ParticipantLangInfo.objects.bulk_create(langs.values())
