"""Simple robolog type detection for PX4 files only."""

import hashlib
import pathlib
from enum import Enum


class RobologType(Enum):
    """Supported robolog types."""
    PX4_ULG_FILE = "px4_ulg_file"
    UNKNOWN = "unknown"


class UnsupportedRobologTypeError(Exception):
    """Raised when robolog type is not supported."""
    
    def __init__(self, robolog_path: str | pathlib.Path) -> None:
        super().__init__(f"Unsupported robolog type: {robolog_path}")


def detect_robolog_type(robolog_path: str | pathlib.Path) -> RobologType:
    """Detect robolog type from file extension."""
    path = pathlib.Path(robolog_path)
    
    if path.suffix.lower() == ".ulg":
        return RobologType.PX4_ULG_FILE
    
    return RobologType.UNKNOWN


def generate_id(robolog_path: str | pathlib.Path) -> str:
    """Generate a unique ID for the robolog based on path and file size."""
    path = pathlib.Path(robolog_path)
    
    # Create ID from file path and size
    path_str = str(path.absolute())
    if path.exists():
        size = path.stat().st_size
        content = f"{path_str}:{size}"
    else:
        content = path_str
    
    return hashlib.md5(content.encode()).hexdigest()[:16]