from metadata.models import Role

roles = {
        "aunt",
        "brother",
        "child",
        "classmate",
        "cousin",
        "family friend",
        "father",
        "grandfather",
        "grandmother",
        "great grandfather",
        "great grandmother",
        "greataunt",
        "greatuncle",
        "linguist",
        "mother",
        "nephew",
        "niece",
        "older brother",
        "older sister",
        "playmate",
        "recorder",
        "relative",
        "researcher",
        "sister",
        "stepfather",
        "teacher",
        "uncle",
        "unknown",
        "greatgrandmother"
    }


def import_roles():
    for role in roles:
        Role.objects.update_or_create(name=role)
