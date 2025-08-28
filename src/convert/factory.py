"""Factory function to create a MessageConverter for PX4 ULog files."""

import pathlib

from src.convert import converter, schema


def make_converter(robolog_path: str | pathlib.Path, type_name: str) -> converter.MessageConverter:
    """Create a MessageConverter for PX4 ULog message types."""
    schema_string = schema.schema_string(robolog_path, type_name)
    encoding = schema.schema_encoding(robolog_path, type_name)

    if encoding == schema.Encoding.PX4ULOG:
        from src.convert import px4ulog
        return px4ulog.MessageConverter(type_name, schema_string)
    else:
        raise schema.UnsupportedSchemaEncodingError(f"Unsupported encoding: {encoding}")