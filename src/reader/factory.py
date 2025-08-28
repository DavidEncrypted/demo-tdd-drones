"""Factory functions to create readers for different reading patterns and robolog types."""

import pathlib

from settings import settings
from src import robolog
from src.reader.frequency import TopicFrequencyReader
from src.reader.topic import TopicMessageReader
from src.reader.type import TypeMessageReader


def make_topic_message_reader(
    robolog_path: str | pathlib.Path, use_cache: bool | None = None
) -> TopicMessageReader:
    """Create a TopicMessageReader for PX4 ULog files."""
    use_cache = use_cache if use_cache is not None else settings.USE_CACHE

    robolog_type = robolog.detect_robolog_type(robolog_path)
    if robolog_type == robolog.RobologType.PX4_ULG_FILE:
        from src.reader.px4.ulg import topic
        return topic.TopicMessageReader(robolog_path, use_cache=use_cache)
    else:
        raise robolog.UnsupportedRobologTypeError(robolog_path)


def make_type_message_reader(
    robolog_path: str | pathlib.Path, use_cache: bool | None = None
) -> TypeMessageReader:
    """Create a TypeMessageReader for PX4 ULog files."""
    use_cache = use_cache if use_cache is not None else settings.USE_CACHE

    robolog_type = robolog.detect_robolog_type(robolog_path)
    if robolog_type == robolog.RobologType.PX4_ULG_FILE:
        from src.reader.px4.ulg import type as type_
        return type_.TypeMessageReader(robolog_path, use_cache=use_cache)
    else:
        raise robolog.UnsupportedRobologTypeError(robolog_path)


def make_topic_frequency_reader(
    robolog_path: str | pathlib.Path, use_cache: bool | None = None
) -> TopicFrequencyReader:
    """Create a TopicFrequencyReader for PX4 ULog files."""
    use_cache = use_cache if use_cache is not None else settings.USE_CACHE

    robolog_type = robolog.detect_robolog_type(robolog_path)
    if robolog_type == robolog.RobologType.PX4_ULG_FILE:
        from src.reader.px4.ulg import frequency
        return frequency.TopicFrequencyReader(robolog_path, use_cache=use_cache)
    else:
        raise robolog.UnsupportedRobologTypeError(robolog_path)
