import random
import string
from metadata.models import Participant


def generate_random_code():
    while True:
        code = ''.join((random.choice(string.ascii_uppercase) for _ in range(3)))
        in_anonymized_codes = Participant.objects.filter(anonymized=code)
        in_shortnames = Participant.objects.filter(short_name=code)
        if not in_anonymized_codes and not in_shortnames:
            return code
