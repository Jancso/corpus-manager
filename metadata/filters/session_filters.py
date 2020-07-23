import re

from django.shortcuts import redirect


def to_days(age):
    if not age:
        return -1

    age = re.match(r"(\d*)(;(\d*)(.(\d*))?)?", str(age))

    years = int(age.group(1))

    if age.group(3):
        months = int(age.group(3))
    else:
        months = 0

    if age.group(5):
        days = int(age.group(5))
    else:
        days = 0

    return years * 365 + months * 30 + days


def with_age_between(sessions, minimum=0, maximum=100):
    result = []
    for session in sessions:
        age = session.get_target_child_age()
        if to_days(minimum) <= to_days(age) <= to_days(maximum):
            result.append(session)

    return result


def filter_sessions(session_filter_form, sessions):
    changed_data = session_filter_form.changed_data

    if 'date_min' in changed_data:
        date_min = session_filter_form.cleaned_data['date_min']
        sessions = sessions.filter(date__gte=date_min)

    if 'date_max' in changed_data:
        date_max = session_filter_form.cleaned_data['date_max']
        sessions = sessions.filter(date__lte=date_max)

    if 'target_child' in changed_data:
        target_child = session_filter_form.cleaned_data['target_child']
        sessions = sessions.filter(
            sessionparticipant__participant__short_name=target_child,
            sessionparticipant__roles__name='child')

    if 'participants' in changed_data:
        participants = session_filter_form.cleaned_data['participants']
        sessions = sessions.filter(
            sessionparticipant__participant__in=participants)

    if 'age_min' in changed_data or 'age_max' in changed_data:
        age_min = session_filter_form.cleaned_data['age_min']
        age_max = session_filter_form.cleaned_data['age_max']
        sessions = with_age_between(sessions, age_min, age_max)

    return sessions
