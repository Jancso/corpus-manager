from metadata.models import Participant
import csv


def import_participants():
    Participant.objects.all().delete()

    participants_path = '/home/anna/Schreibtisch/Semester/acqdiv/dene/Metadata/participants.csv'

    with open(participants_path) as f:
        reader = csv.DictReader(f)
        objs = []
        participants = set()
        for row in reader:

            if row['Short name'] in participants:
                print(row['Short name'], ' is used twice!')
                continue

            objs.append(Participant(
                added_by=row['Added by'] if row['Added by'] else None,
                short_name=row['Short name'] if row['Short name'] else None,
                full_name=row['Full name'] if row['Full name'] else None,
                birth_date=row['Birth date'] if row['Birth date'] else None,
                age=int(row['Age']) if row['Age'] else None,
                gender=row['Gender'] if row['Gender'] else None,
                education=row['Education'] if row['Education'] else None,
                language_biography=row['Language biography'] if row['Language biography'] else None,
                description=row['Description'] if row['Description'] else None,
            ))

            participants.add(row['Short name'])

        Participant.objects.bulk_create(objs)
