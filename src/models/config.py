from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.utils.file import file_load_json


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score_file: str = "scores.json"


def load_config(file_path: str | Path) -> Config:
    if isinstance(file_path, str):
        file_path = Path(file_path)

    data = file_load_json(Path(file_path), expected_root=dict)

    try:
        config = Config(**data)
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"load config: {file_path}")

    return config
