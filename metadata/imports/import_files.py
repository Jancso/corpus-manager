import datetime
import re
from io import StringIO

from metadata.models import File, Recording
import csv


def import_files(file):
    File.objects.all().delete()

    reader = csv.DictReader(StringIO(file))

    files = []

    for row in reader:
        rec_code = row['Recording code']
        print(rec_code)

        row = dict(row)

        # make empty fields None
        for field in row:
            if row[field] == '':
                row[field] = None

        try:
            rec = Recording.objects.get(name=rec_code)
        except Recording.DoesNotExist:
            print(f'Recording {rec_code} does not exist')
            continue

        duration = None
        if row['Duration']:
            hours, minutes, seconds = row['Duration'].split(':')
            duration = datetime.timedelta(
                hours=int(hours),
                minutes=int(minutes),
                seconds=int(seconds)
            )

        file = File.objects.create(
            recording=rec,
            name=row['File name'],
            type=row['Type'],
            format=row['Format'].split('/')[-1],
            duration=duration,
            size=row['Byte size'],
            location=row['Location']
        )

        files.append(file)

    #File.objects.bulk_create(files)

    print('Files import done!')
