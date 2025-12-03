from __future__ import annotations
import json
import os
import csv
from typing import Iterable, List
from .models import Student
from . import db

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_DATA_PATH = os.path.join(DEFAULT_DATA_DIR, "students.json")
USE_DATABASE = True

def ensure_data_dir(path: str = DEFAULT_DATA_DIR) -> None:
    os.makedirs(path, exist_ok=True)

def load_students(path: str = DEFAULT_DATA_PATH) -> List[Student]:
    global USE_DATABASE
    if USE_DATABASE:
        try:
            db.init_database()
            raw = db.get_all_students()
            students = []
            for item in raw:
                try:
                    students.append(Student.from_dict(item))
                except Exception as e:
                    print(f"Warning: Skipping invalid entry: {e}")
            return students
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            USE_DATABASE = False
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
    if USE_DATABASE:
        try:
            student_list = list(students)
            existing_students = db.get_all_students()
            existing_ids = {s['student_id'] for s in existing_students}
            current_ids = {s.student_id for s in student_list}
            
            ids_to_delete = existing_ids - current_ids
            for student_id in ids_to_delete:
                db.delete_student(student_id)
            
            for student in student_list:
                db.insert_student(student.student_id, student.name, student.marks_by_subject)
            return
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    ensure_data_dir(os.path.dirname(path))
    try:
        serializable = [s.to_dict() for s in students]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to save students to file: {e}")

def export_to_json(students: Iterable[Student], path: str) -> None:
    ensure_data_dir(os.path.dirname(path))
    try:
        serializable = [s.to_dict() for s in students]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to export to JSON: {e}")

def export_to_csv(students: Iterable[Student], path: str, subjects: List[str]) -> None:
    ensure_data_dir(os.path.dirname(path))
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name"] + subjects)
            for student in students:
                row = [student.student_id, student.name]
                row.extend(str(student.marks_by_subject.get(subj, 0)) for subj in subjects)
                writer.writerow(row)
    except Exception as e:
        raise IOError(f"Failed to export to CSV: {e}")


