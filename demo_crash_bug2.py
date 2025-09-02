#!/usr/bin/env python3
"""Demo crash for Bug #2: Iterator StopIteration - minimal example for TDD workshop."""

from src.reader.px4.ulg.reader import ULogReader

# Load normal file
reader = ULogReader('data/longflight.ulg')

# This will crash with StopIteration at reader.py:174
# Requesting data from impossible future time creates empty iterator
# When next(iterator) is called on empty iterator, it raises StopIteration
first_topic = reader.topics[0]
messages = list(reader._iter_messages([first_topic], 9999999999.0, 9999999999.0 + 1, False))