from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.utils.file import file_load_json


class Config(BaseModel):
    """
    Defines the configuration schema for the Pac-Man application.

    Attributes:
        score_file: The file path to save and load high scores.
        life: The starting number of player lives.
        width: The logical width of the game board in cells.
        height: The logical height of the game board in cells.
        seed: Random seed for maze generation (-1 for random).
        time: Maximum time allowed for a stage in seconds.
        pacgum: Score value for a standard pacgum.
        super_pacgum: Score value for a super pacgum.
        ghost: Score value for eating a frightened ghost.
    """

    model_config = ConfigDict(extra="forbid")

    score_file: str = "scores.json"
    life: int = 3
    width: int = 15
    height: int = 15
    seed: int = -1
    time: int = 90
    pacgum: int = 10
    super_pacgum: int = 50
    ghost: int = 250


def load_config(file_path: str | Path) -> Config:
    """
    Loads and validates the configuration from a JSON file.

    Args:
        file_path: Path to the JSON configuration file.

    Returns:
        The validated Config object.

    Raises:
        SchemaValidationError: If the JSON data fails validation.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    data = file_load_json(Path(file_path), expected_root=dict)

    try:
        config = Config(**data)
    except ValidationError as e:
        raise SchemaValidationError(e, context=f"load config: {file_path}")

    return config
