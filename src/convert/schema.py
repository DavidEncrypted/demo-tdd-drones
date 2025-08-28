"""Utilities for retrieving schema encodings and strings from PX4 ULog files."""

import functools
import pathlib
from enum import Enum

import yaml

from src import robolog


class UnsupportedSchemaEncodingError(Exception):
    """Raised when a schema encoding is not supported."""


class SchemaNotFoundError(Exception):
    """Raised when a schema of a message type is not found in the robolog."""


class Encoding(Enum):
    """Represent supported schema encodings of message types in a robolog."""

    PX4ULOG = "px4ulog"  # .ulg


@functools.lru_cache(maxsize=128)
def _px4ulog_strings_from_ulg(robolog_path: str | pathlib.Path) -> dict[str, str]:
    """Return a dictionary of message type names to px4ulog strings from a .ulg file."""
    from pyulog import core

    ulog = core.ULog(str(robolog_path), parse_header_only=False)
    schemas = {}
    for type_name, multi_id in [(data.name, data.multi_id) for data in ulog.data_list]:
        topic_data = ulog.get_dataset(type_name, multi_id)
        schema = {field.field_name: field.type_str for field in topic_data.field_data}
        schemas[type_name] = yaml.dump(schema)
    return schemas


def schema_encoding(robolog_path: str | pathlib.Path, type_name: str) -> Encoding:
    """Return the schema encoding of the given message type in the robolog."""
    path = pathlib.Path(robolog_path).absolute()

    robolog_type = robolog.detect_robolog_type(path)
    if robolog_type == robolog.RobologType.PX4_ULG_FILE:
        return Encoding.PX4ULOG
    else:
        raise robolog.UnsupportedRobologTypeError(robolog_path)


def schema_string(robolog_path: str | pathlib.Path, type_name: str) -> str:
    """Return the schema string of the given message type in the PX4 ULog file."""
    path = pathlib.Path(robolog_path).absolute()

    robolog_type = robolog.detect_robolog_type(path)
    if robolog_type == robolog.RobologType.PX4_ULG_FILE:
        try:
            return _px4ulog_strings_from_ulg(path)[type_name]
        except KeyError as err:
            raise SchemaNotFoundError(type_name) from err
    else:
        raise robolog.UnsupportedRobologTypeError(robolog_path)