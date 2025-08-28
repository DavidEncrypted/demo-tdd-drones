"""Base class for reading messages from specific topics in a robolog."""

from collections.abc import Iterator

import pyarrow as pa

from settings import settings
from src.convert.converter import MessageConverter
from src.reader.reader import Reader


class TopicMessageReader(Reader):
    """Base class for reading messages from specific topics in a robolog."""

    def read(
        self,
        topics: list[str] | None = None,
        start_seconds: float | None = None,
        end_seconds: float | None = None,
        peek: bool = False,
        converters: dict[str, MessageConverter] | None = None,
    ) -> pa.Table:
        """Return messages for the specified topics and time range.

        Args:
            topics (list[str] | None, optional): Topics to read from. If None, all topics are read.
            start_seconds (float | None, optional): When to start reading messages.
            end_seconds (float | None, optional): When to stop reading messages.
            peek (bool, optional): If True, only return the first few records.
            converters (dict[str, MessageConverter] | None, optional): Custom converters.

        Returns:
            pa.Table: A PyArrow table containing the topic messages.
        """
        topics = topics or self.topics
        self._raise_if_missing_topics(topics)
        if not topics:
            raise ValueError("No topics specified for reading messages.")

        converters = {**self._converters(topics), **(converters or {})}

        # Build schema
        schema = pa.schema([
            pa.field(settings.ROBOLOG_ID_COLUMN_NAME, pa.string(), nullable=False),
            pa.field(settings.TIMESTAMP_SECONDS_COLUMN_NAME, pa.float64(), nullable=False),
        ])
        for topic in topics:
            schema = schema.append(pa.field(topic, converters[topic].pa_struct, nullable=True))

        # Collect all record batches
        record_batches = []
        for record_batch in self._iter_record_batches(
            topics, start_seconds, end_seconds, False, schema, converters
        ):
            record_batches.append(record_batch)
            if peek:
                break

        # Combine into single table
        if record_batches:
            return pa.Table.from_batches(record_batches)
        else:
            return pa.Table.from_arrays([], schema=schema)

    def _iter_record_batches(
        self,
        topics: list[str],
        start_seconds: float | None,
        end_seconds: float | None,
        ffill: bool,
        schema: pa.Schema,
        converters: dict[str, MessageConverter],
    ) -> Iterator[pa.RecordBatch]:
        """Iterate over record batches for the specified topics and time range."""
        raise NotImplementedError()