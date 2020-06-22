from io import StringIO

from metadata.models import Session, SessionParticipant, Participant, Role
import csv
from django.db.utils import IntegrityError


def import_sessions(file):
    Session.objects.all().delete()

    reader = csv.DictReader(StringIO(file))

    for row in reader:
        row = dict(row)

        # make empty fields None
        for field in row:
            if row[field] == '':
                row[field] = None

        try:
            session = Session.objects.create(
                name=row['Code'],
                date=row['Date'],
                location=row['Location'],
                situation=row['Situation'],
                content=row['Content'],
                comments=row['Comments']
            )
        except IntegrityError:
            name = row['Code']
            print(f'Session name {name} used twice!')
            continue

        if row['Participants and roles'] is not None:

            for part_role in row['Participants and roles'].split(', '):
                part, role = part_role.split(' ', maxsplit=1)

                try:
                    participant = Participant.objects.get(short_name=part)
                except Participant.DoesNotExist:
                    print(f'Participant {part} does not exist!')
                    continue

                session_participant = SessionParticipant.objects.create(
                    participant=participant,
                    session=session
                )

                roles = role[1:-1].split(' & ')
                for role in roles:
                    try:
                        role_obj = Role.objects.get(name=role)
                        session_participant.roles.add(role_obj)
                    except Role.DoesNotExist:
                        print(f'role "{role}" does not exist!')

    print('Sessions import done!')
