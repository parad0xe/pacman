import json
from pathlib import Path
from typing import Any, TypeVar

from src.exceptions.schema import (
    SchemaInvalidJSONFormatError,
    SchemaInvalidJSONRootError,
    SchemaJSONSerializationError,
)
from src.exceptions.storage import (
    StorageError,
    StorageFileNotFoundError,
    StorageFilePermissionError,
)

T = TypeVar("T", bound=list | dict)


def file_load_json(file_path: Path, expected_root: type[T]) -> T:
    """
    Reads a file and parses its content as a JSON list of objects.

    Args:
        file_path: Path to the target JSON file to read.
        expected_root: Expected root type of the JSON file.

    Returns:
        Parsed JSON data.
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

    if content.strip() == "":
        return expected_root()

    try:
        output: T = json.loads(content)

        if not isinstance(output, expected_root):
            raise SchemaInvalidJSONRootError(
                expected=expected_root, context=file_path
            )

        return output
    except json.JSONDecodeError as e:
        raise SchemaInvalidJSONFormatError(
            context=file_path,
            lineno=e.lineno,
        ) from e


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
