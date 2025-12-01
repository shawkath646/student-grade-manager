from __future__ import annotations
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from .config import DB_CONFIG, STUDENTS_TABLE, MARKS_TABLE, PROFILES_TABLE

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
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {PROFILES_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) UNIQUE NOT NULL,
                photo_path VARCHAR(500),
                date_of_birth DATE,
                gender VARCHAR(20),
                blood_group VARCHAR(10),
                religion VARCHAR(50),
                nationality VARCHAR(50),
                address TEXT,
                phone VARCHAR(20),
                email VARCHAR(100),
                session VARCHAR(20),
                department VARCHAR(100),
                semester VARCHAR(20),
                previous_cgpa DECIMAL(3, 2),
                father_name VARCHAR(255),
                father_occupation VARCHAR(100),
                father_phone VARCHAR(20),
                mother_name VARCHAR(255),
                mother_occupation VARCHAR(100),
                mother_phone VARCHAR(20),
                emergency_contact VARCHAR(20),
                FOREIGN KEY (student_id) REFERENCES {STUDENTS_TABLE}(student_id) ON DELETE CASCADE,
                INDEX idx_student_id (student_id)
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
            cursor.execute(f"DELETE FROM {PROFILES_TABLE}")
            cursor.execute(f"DELETE FROM {STUDENTS_TABLE}")
            connection.commit()
            return True
    except Error as e:
        print(f"Error clearing all data: {e}")
        return False

def insert_profile(student_id: str, photo_path: Optional[str] = None, date_of_birth: Optional[str] = None,
                   gender: Optional[str] = None, blood_group: Optional[str] = None, religion: Optional[str] = None,
                   nationality: Optional[str] = None, address: Optional[str] = None, phone: Optional[str] = None,
                   email: Optional[str] = None, session: Optional[str] = None, department: Optional[str] = None,
                   semester: Optional[str] = None, previous_cgpa: Optional[float] = None,
                   father_name: Optional[str] = None, father_occupation: Optional[str] = None,
                   father_phone: Optional[str] = None, mother_name: Optional[str] = None,
                   mother_occupation: Optional[str] = None, mother_phone: Optional[str] = None,
                   emergency_contact: Optional[str] = None) -> bool:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                INSERT INTO {PROFILES_TABLE} (student_id, photo_path, date_of_birth, gender, blood_group, religion,
                                              nationality, address, phone, email, session, department, semester,
                                              previous_cgpa, father_name, father_occupation, father_phone,
                                              mother_name, mother_occupation, mother_phone, emergency_contact)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    photo_path = VALUES(photo_path),
                    date_of_birth = VALUES(date_of_birth),
                    gender = VALUES(gender),
                    blood_group = VALUES(blood_group),
                    religion = VALUES(religion),
                    nationality = VALUES(nationality),
                    address = VALUES(address),
                    phone = VALUES(phone),
                    email = VALUES(email),
                    session = VALUES(session),
                    department = VALUES(department),
                    semester = VALUES(semester),
                    previous_cgpa = VALUES(previous_cgpa),
                    father_name = VALUES(father_name),
                    father_occupation = VALUES(father_occupation),
                    father_phone = VALUES(father_phone),
                    mother_name = VALUES(mother_name),
                    mother_occupation = VALUES(mother_occupation),
                    mother_phone = VALUES(mother_phone),
                    emergency_contact = VALUES(emergency_contact)
            """, (student_id, photo_path, date_of_birth, gender, blood_group, religion, nationality, address,
                  phone, email, session, department, semester, previous_cgpa, father_name, father_occupation,
                  father_phone, mother_name, mother_occupation, mother_phone, emergency_contact))
            connection.commit()
            return True
    except Error as e:
        print(f"Error inserting profile: {e}")
        return False

def get_profile(student_id: str) -> Optional[Dict[str, Any]]:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT student_id, photo_path, date_of_birth, gender, blood_group, religion, nationality,
                       address, phone, email, session, department, semester, previous_cgpa,
                       father_name, father_occupation, father_phone, mother_name, mother_occupation,
                       mother_phone, emergency_contact
                FROM {PROFILES_TABLE} WHERE student_id = %s
            """, (student_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving profile: {e}")
        return None

def update_profile(student_id: str, **kwargs) -> bool:
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            fields = []
            values = []
            allowed_fields = ['photo_path', 'date_of_birth', 'gender', 'blood_group', 'religion', 'nationality',
                            'address', 'phone', 'email', 'session', 'department', 'semester', 'previous_cgpa',
                            'father_name', 'father_occupation', 'father_phone', 'mother_name',
                            'mother_occupation', 'mother_phone', 'emergency_contact']
            for key, value in kwargs.items():
                if key in allowed_fields:
                    fields.append(f"{key} = %s")
                    values.append(value)
            if not fields:
                return False
            values.append(student_id)
            query = f"UPDATE {PROFILES_TABLE} SET {', '.join(fields)} WHERE student_id = %s"
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating profile: {e}")
        return False

