<div align="center">

# 🎓 Student Grade Management System

### Python Desktop Application | Academic Records Management | Data Analytics

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)](LICENSE)

A modern, feature-rich desktop application for managing student academic records with comprehensive grading system, profile management, and statistical analysis.

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Database Schema](#-database-schema)
- [Screenshots](#-screenshots)
- [Authors](#-authors)
- [Course Information](#-course-information)
- [Made By](#-made-by)

---

## 🎯 About

A comprehensive **Student Grade Management System** built with Python and Tkinter for the **final course presentation** of **Application of Programming Language-P** at Sejong University. This desktop application features a modern GUI, MySQL database integration, and advanced profile management capabilities. It streamlines academic record keeping with automated grading, statistical analysis, and comprehensive student profile tracking including personal information, academic history, and family details.

**Course Project**: This system was developed as the final project for the Application of Programming Language-P course (Fall 2024-2025) at Sejong University, instructed by Sejan Mohammad Abrar Shakil.

**Keywords**: Student Management System, Grade Calculator, Academic Records, Python Desktop App, Tkinter GUI, MySQL Database, Educational Software, Grade Analytics, Course Final Project

---

## ✨ Features

### 📊 **Grade Management**

- ✅ **CRUD Operations** - Add, update, delete student records with validation
- ✅ **Multi-Subject Support** - Track marks for English, Math, Science, History, ICT
- ✅ **Auto-Calculation** - Automatic total, average, and grade computation
- ✅ **Search Functionality** - Quick search by student ID or name
- ✅ **Sorting Capabilities** - Sort by ID, Name, Average, or Total marks
- ✅ **Color-Coded Display** - Grade-based row coloring (A=green, B=blue, C=gold, D=orange, F=pink)

### 👤 **Profile Management**

- ✅ **Comprehensive Profiles** - 21 fields including personal, academic, and family information
- ✅ **Photo Upload** - Student profile pictures with 200x200 display
- ✅ **Two-Column Layout** - Compact, card-based design with scrollable content
- ✅ **Fullscreen Support** - Press F11 for fullscreen view, Escape to exit
- ✅ **Modal Windows** - Single profile view at a time for focused interaction
- ✅ **Auto-Hide Scrollbars** - Dynamic scrollbar visibility based on content

**Profile Fields:**
- **Personal Info**: Name, DOB, Gender, Blood Group, Religion, Nationality, Address, Phone, Email
- **Academic Info**: Session, Department, Semester, Previous CGPA
- **Father's Info**: Name, Occupation, Phone
- **Mother's Info**: Name, Occupation, Phone
- **Emergency Contact**: Emergency contact number

### 📈 **Statistical Analysis**

- ✅ **Class Statistics** - Overall class average, pass rate, grade distribution
- ✅ **Subject Analytics** - Subject-wise average performance
- ✅ **Top Performers** - Identify highest-scoring students
- ✅ **Grade Breakdown** - Students count by grade (A, B, C, D, F)
- ✅ **Live Dashboard** - Real-time statistics in the main window

### 💾 **Data Management**

- ✅ **MySQL Database** - Robust data persistence with three tables
- ✅ **JSON Import/Export** - Backup and restore student data
- ✅ **CSV Import/Export** - Excel-compatible data exchange
- ✅ **Auto-Save** - Automatic database updates on changes
- ✅ **Data Validation** - Comprehensive input validation for all fields

### 🎨 **User Experience**

- ✅ **Modern GUI** - Clean, professional interface with Tkinter
- ✅ **Keyboard Shortcuts** - Enter to submit, F11 for fullscreen
- ✅ **Form Auto-Clear** - Automatic form reset after operations
- ✅ **Error Handling** - User-friendly error messages
- ✅ **Menu Bar** - Easy access to all features
- ✅ **Responsive Layout** - Adapts to different screen sizes

---

## 🛠️ Technology Stack

### **Frontend**

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PIL](https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

- **Python 3.13** - Latest Python with modern features
- **Tkinter** - Standard GUI library for Python
- **Pillow (PIL)** - Image processing for profile photos
- **ttk** - Themed widgets for modern UI elements

### **Backend & Database**

<div align="center">

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

</div>

- **MySQL 8.x** - Relational database for data persistence
- **mysql-connector-python** - MySQL driver for Python
- **Firebase Storage** - Profile image storage (optional)

### **Development Tools**

- **VS Code** - Primary development environment
- **Git** - Version control
- **Python Standard Library** - JSON, OS, datetime modules

---

## 📁 Project Structure

```
student-grade-manager/
├── 📂 app/                      # Main application package
│   ├── __init__.py              # Constants (subjects, grade scale)
│   ├── grading.py               # Validation and grading functions
│   ├── manager.py               # Business logic and statistics
│   ├── models.py                # Student data model
│   ├── storage.py               # JSON file operations (legacy)
│   ├── db.py                    # MySQL database operations
│   ├── gui.py                   # Main GUI application
│   ├── main.py                  # Application entry point
│   │
│   └── 📂 windows/              # Modular window components
│       ├── __init__.py          # Package exports
│       ├── profile_window.py   # Student profile viewer
│       └── statistics_window.py # Statistics dashboard
│
├── 📂 scripts/                  # Build and utility scripts
│   ├── build_portable.py        # Portable EXE builder
│   ├── build_exe.spec           # PyInstaller specification
│   ├── run_app.py               # Executable entry point
│   └── README.md                # Build scripts documentation
│
├── 📂 data/                     # Application data (auto-created)
│   ├── students.json            # Student records (JSON format)
│   └── 📂 profiles/             # Student profile images
│
├── 📂 assets/                   # Static assets (optional)
│
├── 📄 README.md                 # Project documentation
├── 📄 CHANGELOG.md              # Version history
├── 📄 CONTRIBUTING.md           # Contribution guidelines
├── 📄 LICENSE                   # MIT License
├── 📄 requirements.txt          # Python dependencies
├── 📄 setup.py                  # Package configuration
├── 📄 launch.bat                # Windows launcher script
└── 📄 run.py                    # Quick launcher script
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13** or higher
- **MySQL 8.x** or higher
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/shawkath646/student-grade-manager.git
cd student-grade-manager

# Install dependencies
pip install mysql-connector-python pillow

# Configure MySQL database
# Update database credentials in app/db.py if needed
# Default: host=localhost, user=root, password=shawkat, database=python_student_grades
```

### Database Setup

```bash
# The application will automatically create the database and tables on first run
# Or manually initialize:
python -c "from app.db import init_database; init_database()"
```

### Running the Application

**Option 1: Portable Executable (Recommended for end users)**
```bash
# Build the portable executable
python scripts/build_portable.py

# Run the executable (no Python installation required)
dist/StudentGradeManager_Portable/StudentGradeManager.exe
```

**Option 2: Development Mode**
```bash
# Method 1: Using launcher script
python run.py

# Method 2: Using batch file (Windows)
launch.bat

# Method 3: Using Python module
python -m app.main
```

---

## 📖 Usage Guide

### Adding Students

1. Click **"Add Student"** button or use the menu
2. Enter Student ID and Name
3. Input marks for all subjects (0-100)
4. Click **Submit** or press **Enter**
5. Student added with auto-calculated total, average, and grade

### Viewing Student Profiles

1. Click **"🔍 View"** in the student row
2. Profile window opens with comprehensive information
3. Press **F11** for fullscreen, **Escape** to exit fullscreen
4. Click **Close** to return to main window

### Updating Student Information

1. Search for the student
2. Click **Update** in the student row
3. Modify marks or information
4. Click **Submit** to save changes

### Statistical Analysis

1. Click **"Statistics"** button in the menu or toolbar
2. View class average, pass rate, and grade distribution
3. Check subject-wise averages
4. See top and bottom performers

### Importing/Exporting Data

**Import:**
- **File → Import JSON** - Import from JSON file
- **File → Import CSV** - Import from CSV file

**Export:**
- **File → Export to CSV** - Export all records to CSV

### Keyboard Shortcuts

- **Enter** - Submit form
- **F11** - Toggle fullscreen (in profile window)
- **Escape** - Exit fullscreen

---

## 🗄️ Database Schema

### **students** Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | VARCHAR(20) | Primary key, student ID |
| `name` | VARCHAR(100) | Student full name |

### **student_marks** Table

| Column | Type | Description |
|--------|------|-------------|
| `student_id` | VARCHAR(20) | Foreign key to students.id |
| `english` | INT | English marks (0-100) |
| `math` | INT | Math marks (0-100) |
| `science` | INT | Science marks (0-100) |
| `history` | INT | History marks (0-100) |
| `ict` | INT | ICT marks (0-100) |
| `total` | INT | Total marks (auto-calculated) |
| `average` | DECIMAL(5,2) | Average marks (auto-calculated) |
| `grade` | CHAR(1) | Letter grade (auto-calculated) |

### **student_profiles** Table

| Column | Type | Description |
|--------|------|-------------|
| `student_id` | VARCHAR(20) | Foreign key to students.id |
| `photo_path` | TEXT | Profile photo file path |
| `date_of_birth` | DATE | Date of birth |
| `gender` | VARCHAR(10) | Male/Female |
| `blood_group` | VARCHAR(5) | Blood group (A+, O-, etc.) |
| `religion` | VARCHAR(50) | Religion |
| `nationality` | VARCHAR(50) | Nationality |
| `address` | TEXT | Full address |
| `phone` | VARCHAR(20) | Contact number |
| `email` | VARCHAR(100) | Email address |
| `session` | VARCHAR(20) | Academic session |
| `department` | VARCHAR(100) | Department name |
| `semester` | VARCHAR(20) | Current semester |
| `previous_cgpa` | DECIMAL(3,2) | Previous CGPA |
| `father_name` | VARCHAR(100) | Father's name |
| `father_occupation` | VARCHAR(100) | Father's occupation |
| `father_phone` | VARCHAR(20) | Father's phone |
| `mother_name` | VARCHAR(100) | Mother's name |
| `mother_occupation` | VARCHAR(100) | Mother's occupation |
| `mother_phone` | VARCHAR(20) | Mother's phone |
| `emergency_contact` | VARCHAR(20) | Emergency contact number |

---

## 📸 Screenshots

*Screenshots coming soon...*

---

## 👨‍💻 Authors

**Maruf Shawkat Hossain**
- Student ID: 25013492
- GitHub: [@shawkath646](https://github.com/shawkath646)
- Email: shawkath646@gmail.com

**Hasan Md Mahadi**
- Student ID: 25013422

---

## 🎓 Course Information

**Project Type**: Final Course Presentation

**Course**: Application of Programming Language-P

**Course Code**: TBD

**Instructor**: Sejan Mohammad Abrar Shakil

**Institution**: Sejong University

**Department**: Computer Science and Engineering

**Semester**: Fall 2024-2025

**Presentation Date**: December 2024

**Project Duration**: October 2024 - December 2024

---

**Project Objectives:**
- Demonstrate proficiency in Python programming
- Apply object-oriented programming principles
- Implement database integration with MySQL
- Create user-friendly GUI applications with Tkinter
- Develop comprehensive data management systems
- Apply software engineering best practices


## 🏢 Powered By

<div align="center">

<img src="https://cloudburstlab.vercel.app/api/branding/logo?variant=transparent" alt="Cloudburst Lab" width="200" />

<br />

**Cloudburst Lab** is a digital innovation studio focused on creating exceptional web and mobile applications. We specialize in modern JavaScript frameworks, cloud technologies, and user-centric design principles.

</div>

## 📄 License

This project is developed for academic purposes as part of the **Application of Programming Language** course.

© 2024-2025 Maruf Shawkat Hossain & Hasan Md Mahadi. All rights reserved.

---

## 🙏 Acknowledgments

- **Python Software Foundation** - For the Python programming language
- **Tkinter Team** - For the GUI toolkit
- **MySQL** - For the database system
- **Sejong University** - For the academic support
- **Instructor Sejan Mohammad Abrar Shakil** - For guidance and mentorship

---

## 📊 Project Stats

![Python](https://img.shields.io/badge/Language-Python_3.13-blue?style=flat-square&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![Database](https://img.shields.io/badge/Database-MySQL_8.0-orange?style=flat-square&logo=mysql)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.0-blue?style=flat-square)

---

<div align="center">

### ⭐ Star this repository if you find it helpful

</div>



