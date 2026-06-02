import uuid


def unique_id() -> str:
    """
    Generates a unique string identifier.

    Returns:
        A unique UUID string.
    """
    return str(uuid.uuid4())
