from metadata.models import Participant, ParticipantLangInfo, Language
import csv


def import_participants():
    Participant.objects.all().delete()

    participants_path = '/home/anna/Schreibtisch/Semester/acqdiv/dene/Metadata/participants.csv'

    with open(participants_path) as f:
        reader = csv.DictReader(f)
        participant_objects = []
        lang_info_objects = []

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

            participant = Participant.objects.create(added_by=row['Added by'],
                                      short_name=row['Short name'],
                                      full_name=row['Full name'],
                                      birth_date=row['Birth date'],
                                      age=row['Age'], gender=row['Gender'],
                                      education=row['Education'],
                                      language_biography=row[
                                          'Language biography'],
                                      description=row['Description'])

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
