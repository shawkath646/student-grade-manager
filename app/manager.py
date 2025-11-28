from __future__ import annotations
from typing import Dict, Iterable, List, Optional
from .models import Student

class StudentManager:
    def __init__(self, students: Optional[Iterable[Student]] = None) -> None:
        self._students: Dict[str, Student] = {}
        if students:
            for s in students:
                self._students[s.student_id] = s

    def list_students(self) -> List[Student]:
        return list(self._students.values())

    def get(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)

    def add_or_update(self, student: Student) -> None:
        self._students[student.student_id] = student

    def delete(self, student_id: str) -> bool:
        return self._students.pop(student_id, None) is not None

    def search(self, query: str) -> List[Student]:
        q = query.strip().lower()
        return [s for s in self._students.values() if q in s.student_id.lower() or q in s.name.lower()]

    def class_average(self) -> float:
        students = self.list_students()
        if not students:
            return 0.0
        return sum(s.average() for s in students) / len(students)

    def top_performers(self, n: int = 3) -> List[Student]:
        return sorted(self.list_students(), key=lambda s: s.average(), reverse=True)[:n]

    def bottom_performers(self, n: int = 3) -> List[Student]:
        return sorted(self.list_students(), key=lambda s: s.average())[:n]

    def count_students(self) -> int:
        return len(self._students)

    def students_by_grade(self) -> Dict[str, int]:
        from . import DEFAULT_GRADE_SCALE
        from .grading import compute_grade
        grade_counts: Dict[str, int] = {}
        for student in self.list_students():
            grade = compute_grade(student.average(), DEFAULT_GRADE_SCALE)
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        return grade_counts

    def pass_rate(self) -> float:
        students = self.list_students()
        if not students:
            return 0.0
        from . import DEFAULT_GRADE_SCALE
        from .grading import compute_grade
        passed = sum(1 for s in students if compute_grade(s.average(), DEFAULT_GRADE_SCALE) != 'F')
        return (passed / len(students)) * 100

    def subject_averages(self) -> Dict[str, float]:
        students = self.list_students()
        if not students:
            return {}
        subject_totals: Dict[str, float] = {}
        subject_counts: Dict[str, int] = {}
        for student in students:
            for subject, mark in student.marks_by_subject.items():
                subject_totals[subject] = subject_totals.get(subject, 0.0) + mark
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
        return {subject: total / subject_counts[subject] for subject, total in subject_totals.items() if subject_counts[subject] > 0}

    def get_students_in_range(self, min_avg: float, max_avg: float) -> List[Student]:
        return [s for s in self.list_students() if min_avg <= s.average() <= max_avg]

    def statistics(self) -> Dict[str, object]:
        return {
            "total_students": self.count_students(),
            "class_average": self.class_average(),
            "pass_rate": self.pass_rate(),
            "students_by_grade": self.students_by_grade(),
            "subject_averages": self.subject_averages(),
            "top_performers": [(s.name, s.average()) for s in self.top_performers(3)],
            "bottom_performers": [(s.name, s.average()) for s in self.bottom_performers(3)],
        }

