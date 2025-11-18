from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def clamp_mark(value: float) -> float:
    """Clamp mark value between 0 and 100."""
    if value < 0:
        return 0.0
    if value > 100:
        return 100.0
    return float(value)


def compute_grade(average: float, grade_scale: Sequence[Tuple[float, str]]) -> str:
    """Compute letter grade based on average."""
    for threshold, grade in grade_scale:
        if average >= threshold:
            return grade
    return grade_scale[-1][1] if grade_scale else "F"


def validate_marks(marks: Iterable[float]) -> None:
    """Validate that all marks are numeric and within 0-100 range."""
    for m in marks:
        if not isinstance(m, (int, float)):
            raise ValueError("Marks must be numeric.")
        if m < 0 or m > 100:
            raise ValueError("Each mark must be between 0 and 100.")


def validate_student_id(student_id: str) -> None:
    """Validate student ID format."""
    if not student_id or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")
    if len(student_id.strip()) > 50:
        raise ValueError("Student ID cannot exceed 50 characters.")


def validate_student_name(name: str) -> None:
    """Validate student name."""
    if not name or not name.strip():
        raise ValueError("Student name cannot be empty.")
    if len(name.strip()) > 100:
        raise ValueError("Student name cannot exceed 100 characters.")
    # Check for only whitespace
    if not name.strip():
        raise ValueError("Student name cannot be only whitespace.")
    # Check for valid characters (allow letters, spaces, hyphens, apostrophes)
    import re
    if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
        raise ValueError("Student name can only contain letters, spaces, hyphens, and apostrophes.")


def validate_float_input(value: str, field_name: str = "value") -> float:
    """Validate and convert string input to float."""
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    try:
        float_val = float(value)
        if float_val < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        if float_val > 100:
            raise ValueError(f"{field_name} cannot exceed 100.")
        return float_val
    except ValueError as e:
        raise ValueError(f"{field_name} must be a valid number. {str(e)}")
