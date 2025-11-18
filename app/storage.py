from __future__ import annotations

import json
import os
from typing import Dict, Iterable, List

from .models import Student


DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_DATA_PATH = os.path.join(DEFAULT_DATA_DIR, "students.json")


def ensure_data_dir(path: str = DEFAULT_DATA_DIR) -> None:
    """Create the data directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def load_students(path: str = DEFAULT_DATA_PATH) -> List[Student]:
    """Load students from JSON file with validation."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise ValueError("Invalid file format: expected a list of students")
        students = []
        for idx, item in enumerate(raw):
            try:
                students.append(Student.from_dict(item))
            except Exception as e:
                print(f"Warning: Skipping invalid entry at index {idx}: {e}")
        return students
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file: {e}")
    except Exception as e:
        raise IOError(f"Failed to load students from file: {e}")


def save_students(students: Iterable[Student], path: str = DEFAULT_DATA_PATH) -> None:
    """Save students to JSON file with validation."""
    ensure_data_dir(os.path.dirname(path))
    try:
        serializable = [s.to_dict() for s in students]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to save students to file: {e}")

