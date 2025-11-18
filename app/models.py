from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Student:
    student_id: str
    name: str
    marks_by_subject: Dict[str, float] = field(default_factory=dict)

    def total(self) -> float:
        return float(sum(self.marks_by_subject.values()))

    def average(self) -> float:
        if not self.marks_by_subject:
            return 0.0
        return self.total() / len(self.marks_by_subject)

    def to_dict(self) -> Dict[str, object]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "marks_by_subject": dict(self.marks_by_subject),
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> "Student":
        return Student(
            student_id=str(data.get("student_id", "")),
            name=str(data.get("name", "")),
            marks_by_subject={
                str(k): float(v) for k, v in dict(data.get("marks_by_subject", {})).items()
            },
        )




