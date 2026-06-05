from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, ValidationError

from src.exceptions.schema import SchemaValidationError
from src.utils.common import json_parse_comments, load_json
from src.utils.file import file_load_plain


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score_file: str = "scores.json"
    life: int = Field(default=3, ge=1, le=10)
    width: int = Field(default=15, ge=10, le=20)
    height: int = Field(default=15, ge=10, le=20)
    seed: int = Field(default=-1, ge=-1)
    time: int = Field(default=90, ge=1, le=3600)
    pacgum_points: int = Field(default=10, ge=0, le=2000)
    super_pacgum_points: int = Field(default=50, ge=0, le=4000)
    ghost_points: int = Field(default=250, ge=0, le=8000)


def load_config(file_path: str | Path) -> Config:
    """
    Loads configuration from JSON with fallbacks:
    - Missing keys -> default values
    - Invalid values -> default values
    Returns (config, warnings).
    """
    path = Path(file_path)
    raw_text = file_load_plain(path)
    parsed_text = json_parse_comments(raw_text)
    data: dict[str, Any] = load_json(parsed_text, expected_root=dict)

    defaults = Config()
    config = Config()
    warnings: list[str] = []

    provided_keys = set(data.keys())
    model_keys = set(Config.model_fields.keys())

    for extra_key in sorted(provided_keys - model_keys):
        warnings.append(f"[WARN] Unknown config key '{extra_key}' ignored.")

    for key, field in Config.model_fields.items():
        if key in provided_keys:
            continue
        warnings.append(
            f"[WARN] Missing config key '{key}', using default "
            f"{getattr(defaults, key)!r}."
        )

    for key, value in data.items():
        if key not in Config.model_fields:
            continue

        candidate = config.model_dump()
        candidate[key] = value

        try:
            config = Config.model_validate(candidate)
        except ValidationError as e:
            print(SchemaValidationError(e))
            print(
                f"- [WARN] Invalid value for '{key}'={value!r}, "
                f"using default ({getattr(defaults, key)!r}). "
            )

    for warn in warnings:
        print(warn)

    return config
