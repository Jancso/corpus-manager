import csv
from io import StringIO
from .models import Recording, Task

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

def import_(file):
    file = file.read().decode()

    csv_data = csv.DictReader(StringIO(file), fieldnames=FIELDNAMES)
    for row in csv_data:
        print(row['recording name'])
        rec, _ = Recording.objects.update_or_create(
            name=row['recording name']
        )

        for task_name_i, task_name_h in Task.NAME_CHOICES:
            task, _ = Task.objects.update_or_create(
                recording=rec,
                name=task_name_i
            )