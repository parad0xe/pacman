import json
from pathlib import Path
from typing import Any

from src.exceptions.schema import SchemaJSONSerializationError
from src.exceptions.storage import (
    StorageError,
    StorageFileNotFoundError,
    StorageFilePermissionError,
)
from src.utils.common import JsonRootType, load_json


def file_load_plain(file_path: Path) -> str:
    """
    Reads a file.

    Args:
        file_path: Path to the target file to read.

    Returns:
        File content as a string.
    """

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        raise StorageFileNotFoundError(file_path) from e
    except PermissionError as e:
        raise StorageFilePermissionError(file_path) from e
    except OSError as e:
        raise StorageError(str(file_path)) from e

    return content


def file_load_json(
    file_path: Path,
    expected_root: type[JsonRootType],
) -> JsonRootType:
    """
    Reads a file and parses its content as a JSON list of objects.

    Args:
        file_path: Path to the target JSON file to read.
        expected_root: Expected root type of the JSON file.

    Returns:
        Parsed JSON data.
    """

    content = file_load_plain(file_path)
    return load_json(content, expected_root=expected_root)


def file_write_json(
    file_path: Path, data: list[Any] | dict[Any, Any] | str
) -> None:
    """
    Writes data to a JSON file.

    Args:
        file_path: Destination path.
        data: Data structure or raw JSON string to write.

    Raises:
        StorageFilePermissionError: If parent dir cannot be created or file
            cannot be written.
        SchemaJSONSerializationError: If data cannot be serialized.
        StorageFileNotFoundError: If the file path is invalid.
        StorageError: For other OS-level errors.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise StorageFilePermissionError(file_path) from e
    except OSError as e:
        raise StorageError(None, file_path) from e

    try:
        str_json = (
            data if isinstance(data, str) else json.dumps(data, indent=4)
        )
    except TypeError as e:
        raise SchemaJSONSerializationError(
            reason=str(e), context=file_path
        ) from e

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str_json)
    except FileNotFoundError as e:
        raise StorageFileNotFoundError(file_path) from e
    except PermissionError as e:
        raise StorageFilePermissionError(file_path) from e
    except OSError as e:
        raise StorageError(None, file_path) from e
