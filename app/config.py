from __future__ import annotations
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "11111111"),
    "database": os.getenv("DB_NAME", "python_student_grades"),
}

STUDENTS_TABLE = "students"
MARKS_TABLE = "student_marks"
