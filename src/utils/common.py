import json
import re
import uuid
from typing import Any, TypeVar, cast

from src.exceptions.schema import (
    SchemaInvalidJSONFormatError,
    SchemaInvalidJSONRootError,
)

JsonRootType = TypeVar("JsonRootType", bound=list[Any] | dict[Any, Any])


def unique_id() -> str:
    """
    Generates a unique string identifier.

    Returns:
        A unique UUID string.
    """
    return str(uuid.uuid4())


def load_json(
    str_data: str,
    expected_root: type[JsonRootType],
) -> JsonRootType:
    """
    Parses a JSON string.

    Args:
        str_data: The raw JSON text payload to be parsed.
        expected_root: The expected root structure of the JSON.

    Returns:
        The safely parsed JSON data structure.

    Raises:
        SchemaInvalidJSONRootError: If the root type mismatches expectations.
        SchemaInvalidJSONFormatError: If the string is not valid JSON.
    """

    if str_data.strip() == "":
        return cast(JsonRootType, expected_root())

    try:
        output: JsonRootType = json.loads(str_data)

        if not isinstance(output, expected_root):
            raise SchemaInvalidJSONRootError(
                expected=cast(Any, expected_root), context=str_data
            )

        return output
    except json.JSONDecodeError as e:
        raise SchemaInvalidJSONFormatError(
            context=str_data,
            lineno=e.lineno,
        ) from e


def json_parse_comments(data: str) -> str:
    """
    Strips comments and trailing commas from raw JSON string data.

    Args:
        data: The raw JSON text content containing potential comments.

    Returns:
        The cleaned JSON string ready for standard parsing.
    """

    data = data.strip()

    if data == "":
        return ""

    lines = data.split("\n")
    valid_lines: list[str] = []
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        valid_lines.append(line)

    # remove trailing commas
    str_lines: str = "\n".join(valid_lines)

    return re.sub(
        r"([^\"]*|\".*\"),([\t\r\n ]*)}([^\"]?)",
        r"\1\2}\3",
        str_lines,
        flags=re.MULTILINE,
    )
