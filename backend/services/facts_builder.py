from database.db_manager import get_facts


def build_facts(profession: str | None = None):
    """Returns facts stored in SQLite. Profession-specific facts are preferred."""
    if profession:
        facts = get_facts(profession)
        if facts:
            return facts
    return get_facts()
