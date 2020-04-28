from metadata.models import Session, SessionParticipant, Participant
import csv
from django.db.utils import IntegrityError


def import_sessions():
    Session.objects.all().delete()

    sessions_path = '/home/anna/Schreibtisch/Semester/acqdiv/dene/Metadata/sessions.csv'

    with open(sessions_path) as f:
        reader = csv.DictReader(f)

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
                session_participants = []

                for part_role in row['Participants and roles'].split(', '):
                    part, role = part_role.split(' ', maxsplit=1)
                    # TODO: (mother & recorder)
                    role = role[1:-1].split('&')[0]

                    try:
                        participant = Participant.objects.get(short_name=part)
                    except Participant.DoesNotExist:
                        print(f'Participant {part} does not exist!')
                        continue

                    session_participant = SessionParticipant(
                        participant=participant,
                        session=session,
                        role=role
                    )

                    session_participants.append(session_participant)

                SessionParticipant.objects.bulk_create(session_participants)
