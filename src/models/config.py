from pathlib import Path

from pydantic import BaseModel, Field, ConfigDict, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.utils.file import file_load_json


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score_file: str = "scores.json"
    life: int = Field(default=3, ge=1)
    width: int = Field(default=15, ge=10, le=25)
    height: int = Field(default=15, ge=10, le=25)
    seed: int = Field(default=-1, ge=-1)
    time: int = Field(default=90, ge=1)
    pacgum: int = Field(default=10, ge=0)
    super_pacgum: int = Field(default=50, ge=0)
    ghost: int = Field(default=250, ge=0)


def load_config(file_path: str | Path) -> Config:
    if isinstance(file_path, str):
        file_path = Path(file_path)

    data = file_load_json(Path(file_path), expected_root=dict)

    try:
        config = Config(**data)
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"load config: {file_path}")

    return config
