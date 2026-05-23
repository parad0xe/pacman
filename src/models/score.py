from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.utils.file import file_load_json, file_write_json


class Score(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pseudo: str
    score: int


class Highscores(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scores: list[Score] = Field(default_factory=list)


def save_highscores(file_path: str | Path, scores: Highscores) -> None:
    if isinstance(file_path, str):
        file_path = Path(file_path)

    try:
        file_write_json(file_path, scores.model_dump())
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"save highscores: {file_path}")


def load_highscores(file_path: str | Path) -> Highscores:
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.is_file():
        return Highscores()

    data = file_load_json(Path(file_path), expected_root=dict)

    try:
        highscores = Highscores(**data)
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"load highscores: {file_path}")

    return highscores
