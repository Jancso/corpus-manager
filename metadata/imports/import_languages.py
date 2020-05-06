import csv

import requests

from metadata.models import Language


def import_languages_from_SIL():
    Language.objects.all().delete()

    url = 'https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab'

    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        languages = []

        reader = csv.reader(decoded_content.splitlines(), delimiter='\t')
        for row in reader:
            iso = row[0]
            name = row[6]

            languages.append(Language(iso_code=iso, name=name))

        Language.objects.bulk_create(languages)


def import_languages():
    languages = [
        ('Dene', 'chp'),
        ('English', 'eng'),
        ('German', 'deu'),
        ('French', 'fra')
    ]

    for name, iso_code in languages:
        Language.objects.update_or_create(iso_code=iso_code, name=name)
