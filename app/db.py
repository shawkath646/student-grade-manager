from __future__ import annotations
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from .config import DB_CONFIG, STUDENTS_TABLE, MARKS_TABLE

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

def init_database() -> None:
    try:
        config_without_db = DB_CONFIG.copy()
        db_name = config_without_db.pop("database")
        connection = mysql.connector.connect(**config_without_db)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {STUDENTS_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_student_id (student_id),
                INDEX idx_name (name)
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {MARKS_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                marks DECIMAL(5, 2) NOT NULL,
                FOREIGN KEY (student_id) REFERENCES {STUDENTS_TABLE}(student_id) ON DELETE CASCADE,
                UNIQUE KEY unique_student_subject (student_id, subject),
                INDEX idx_student_id (student_id),
                INDEX idx_subject (subject)
            )
        """)
        connection.commit()
        print("Database initialized successfully!")
    except Error as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_student(student_id: str, name: str, marks_by_subject: Dict[str, float]) -> bool:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                INSERT INTO {STUDENTS_TABLE} (student_id, name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE name = %s
            """, (student_id, name, name))
            cursor.execute(f"DELETE FROM {MARKS_TABLE} WHERE student_id = %s", (student_id,))
            for subject, marks in marks_by_subject.items():
                cursor.execute(f"""
                    INSERT INTO {MARKS_TABLE} (student_id, subject, marks)
                    VALUES (%s, %s, %s)
                """, (student_id, subject, marks))
            connection.commit()
            return True
    except Error as e:
        print(f"Error inserting student: {e}")
        return False

def get_student(student_id: str) -> Optional[Dict[str, Any]]:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT student_id, name FROM {STUDENTS_TABLE} WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            if not student:
                return None
            cursor.execute(f"SELECT subject, marks FROM {MARKS_TABLE} WHERE student_id = %s", (student_id,))
            marks = cursor.fetchall()
            student['marks_by_subject'] = {row['subject']: float(row['marks']) for row in marks}
            return student
    except Error as e:
        print(f"Error retrieving student: {e}")
        return None

def get_all_students() -> List[Dict[str, Any]]:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT student_id, name FROM {STUDENTS_TABLE}")
            students = cursor.fetchall()
            cursor.execute(f"SELECT student_id, subject, marks FROM {MARKS_TABLE}")
            all_marks = cursor.fetchall()
            marks_dict = {}
            for mark in all_marks:
                sid = mark['student_id']
                if sid not in marks_dict:
                    marks_dict[sid] = {}
                marks_dict[sid][mark['subject']] = float(mark['marks'])
            for student in students:
                sid = student['student_id']
                student['marks_by_subject'] = marks_dict.get(sid, {})
            return students
    except Error as e:
        print(f"Error retrieving all students: {e}")
        return []

def delete_student(student_id: str) -> bool:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {STUDENTS_TABLE} WHERE student_id = %s", (student_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting student: {e}")
        return False

def clear_all_data() -> bool:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {MARKS_TABLE}")
            cursor.execute(f"DELETE FROM {STUDENTS_TABLE}")
            connection.commit()
            return True
    except Error as e:
        print(f"Error clearing data: {e}")
        return False

