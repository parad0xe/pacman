from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.exceptions.storage import (
    StorageError,
    StorageFileNotFoundError,
    StorageFilePermissionError,
)
from src.utils.file import file_load_json, file_write_json

MAX_HIGHSCORES = 10


class Score(BaseModel):
    """
    Represents a single high score entry.

    Attributes:
        pseudo: The username or alias of the player.
        score: The numerical score achieved.
    """

    model_config = ConfigDict(extra="forbid")

    pseudo: str
    score: int


class Highscores(BaseModel):
    """
    Represents the collection of high scores.

    Attributes:
        scores: The list of stored Score entries.
    """

    model_config = ConfigDict(extra="forbid")

    scores: list[Score] = Field(default_factory=list)


def save_highscores(file_path: str | Path, scores: Highscores) -> None:
    """
    Saves the high score collection to a JSON file.

    Args:
        file_path: Destination path for the JSON file.
        scores: The highscores data object to persist.

    Raises:
        SchemaValidationError: If serialization or validation fails.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    scores.scores = scores.scores[-MAX_HIGHSCORES:]

    try:
        file_write_json(file_path, scores.model_dump())
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"save highscores: {file_path}")


def load_highscores(file_path: str | Path) -> Highscores:
    """
    Loads the high score collection from a JSON file.

    Args:
        file_path: Source path of the JSON file.

    Returns:
        The loaded Highscores object, or an empty one if missing.

    Raises:
        SchemaValidationError: If parsing or validation fails.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.is_file():
        return Highscores()

    try:
        data = file_load_json(Path(file_path), expected_root=dict)
    except StorageError as e:
        raise e
    except Exception:
        print(
            f"[WARN] Highscores file '{file_path}' is corrupt. "
            "Regenerating new empty highscores file..."
        )
        return Highscores()

    try:
        highscores = Highscores(**data)
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"load highscores: {file_path}")

    return highscores
