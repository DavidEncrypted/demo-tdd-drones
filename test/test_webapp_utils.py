"""Tests for webapp utility functions."""

import time
from unittest.mock import patch

import pytest

from src.webapp.utils import stream


def test_stream_yields_all_characters():
    """Test that stream yields all characters from input text."""
    text = "hello"
    result = list(stream(text, seconds=0))  # No delay for testing
    expected = ["h", "e", "l", "l", "o"]
    assert result == expected


def test_stream_with_empty_string():
    """Test that stream handles empty string correctly."""
    text = ""
    result = list(stream(text, seconds=0))
    assert result == []


def test_stream_with_single_character():
    """Test that stream works with single character."""
    text = "x"
    result = list(stream(text, seconds=0))
    assert result == ["x"]


@patch('time.sleep')
def test_stream_calls_sleep_with_correct_delay(mock_sleep):
    """Test that stream calls time.sleep with the specified delay."""
    text = "ab"
    delay = 0.05
    
    list(stream(text, seconds=delay))
    
    # Should call sleep once for each character
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(delay)


def test_stream_default_delay():
    """Test that stream uses default delay of 0.02 seconds."""
    text = "a"
    start_time = time.time()
    list(stream(text))
    end_time = time.time()
    
    # Should take at least the default delay time
    assert end_time - start_time >= 0.02


def test_stream_is_iterator():
    """Test that stream returns an iterator."""
    text = "test"
    result = stream(text, seconds=0)
    
    # Should be an iterator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')