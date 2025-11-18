## Student Grade Management System

A Python 3 application with a Tkinter GUI to manage student academic records: add/update/delete students, calculate totals/averages/grades, search, show class stats, and persist data to JSON.

### Features
**Core Features:**
- Add, update, delete student records (ID, name, multiple subject marks)
- Automatic total, average, and grade calculation
- Search by ID or name
- Class average and top performers
- JSON-based data persistence
- Automatic save on data changes

**Enhanced Features:**
- **Import/Export:** Import from JSON and CSV files, export to CSV
- **File Format Validation:** Validates JSON structure and CSV column matching before import
- **Comprehensive input validation** (ID, name, marks)
- **Enhanced Styling:** 
  - Color-coded rows based on grades (A=green, B=blue, C=gold, D=orange, F=pink)
  - Improved table layout with horizontal and vertical scrollbars
  - Better formatted numeric values
- **Detailed statistics window** with:
  - Students by grade breakdown
  - Subject-wise averages
  - Top and bottom performers
  - Pass rate calculation
  - Full class statistics
- **Sorting capabilities** (by ID, Name, Average, Total)
- **Form auto-clear** after operations
- **Keyboard shortcuts** (Enter to submit)
- **Menu bar** for easy access to all features
- **Enhanced error handling** and user feedback
- **Live statistics** showing class average, top performers, and total count

### Tech
- Python 3 (standard library)
- Tkinter for GUI
- JSON, OS

### Project Structure
```
app/
  __init__.py         # Constants (subjects, grade scale)
  grading.py          # Validation and grading functions
  manager.py          # Business logic and statistics
  models.py           # Student data model
  storage.py          # File operations
  gui.py             # Main GUI application
  main.py             # Entry point
data/
  students.json           # Data file (auto-created)
  students.sample.json    # Sample JSON import file
  students.sample.csv     # Sample CSV import file
README.md
```

### Getting Started
1. Ensure Python 3.10+ is installed.
2. Run the app:
```bash
python -m app.main
```

The app will create `data/students.json` on first save. 

**Importing Sample Data:**
- You can import sample data using File → Import JSON or File → Import CSV
- Sample files are provided in the `data/` folder:
  - `students.sample.json` - JSON format
  - `students.sample.csv` - CSV format with headers

### Subjects and Grading
- Default subjects: English, Math, Science, History, ICT
- Grade scale (default):
  - A: average ≥ 80
  - B: average ≥ 70
  - C: average ≥ 60
  - D: average ≥ 50
  - F: otherwise

### Credits
Submitted by: MARUF SHAWKAT HOSSAIN (25013492) & HASAN MD MAHADI (25013422)

Course: Application of Programming Language-P

Instructor: SEJAN MOHAMMAD ABRAR SHAKIL



