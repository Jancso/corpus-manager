from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from metadata.models import Language

import requests
import csv


@login_required
def language_list_view(request):
    languages = Language.objects.order_by('name')
    context = {'languages': languages}
    return render(request,
                  'metadata/language/language_list.html', context)


def update_languages():
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


@login_required
def language_list_update_view(_):
    update_languages()
    return redirect('metadata:language-list')
