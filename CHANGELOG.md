# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-01

### Added

#### Profile Management System
- Comprehensive student profiles with 21 fields
- Profile photo support with image upload
- Two-column card-based layout for profile display
- Fullscreen mode (F11) for profile viewing
- Modal profile windows with single-instance restriction
- Six organized sections: Photo, Personal Info, Academic Info, Father's Info, Mother's Info, Emergency Contact

#### Database Integration
- MySQL database with three normalized tables (students, student_marks, student_profiles)
- Database initialization script
- Foreign key relationships for data integrity
- Transaction management for database operations
- Profile data management (insert, update, retrieve)

#### UI/UX Enhancements
- Auto-hide scrollbars that appear only when needed
- Color-coded student rows based on grades
- Improved profile button styling (single-click access)
- Resizable main window
- Enhanced form layouts and spacing

#### Code Organization
- Modular code structure with `app/windows/` package
- Separated ProfileWindow into dedicated module
- Separated StatisticsWindow into dedicated module
- Improved code maintainability and reusability

#### Documentation
- Comprehensive README.md with professional formatting
- PRESENTATION.md for 10-minute course presentation
- Project structure documentation
- Database schema documentation
- Feature descriptions and usage guide

### Changed
- Window size optimized (900x700 for profile window)
- Profile display layout from single-column to two-column
- Code organization from monolithic to modular
- Data persistence from JSON-only to MySQL primary with JSON backup

### Fixed
- Profile button styling issue (removed incorrect tag application)
- Scrollbar visibility logic
- Profile window multiple instance issue
- Database connection management

## [1.0.0] - 2024-11-04

### Added

#### Core Features
- Student management (Add, Update, Delete)
- Grade calculation system with five subjects (English, Math, Science, History, ICT)
- Automatic total, average, and letter grade calculation
- Search functionality by ID or name
- Sort capabilities (by ID, Name, Average, Total)

#### Statistics
- Class average calculation
- Top performers identification
- Grade distribution breakdown
- Subject-wise averages
- Pass rate calculation

#### Data Management
- JSON-based data persistence
- Import from JSON files
- Import from CSV files
- Export to CSV
- Sample data files included

#### User Interface
- Tkinter-based GUI
- Input form with validation
- Student table with scrollbars
- Menu bar for easy navigation
- Live statistics display
- Color-coded grade rows

#### Validation
- Student ID validation
- Name validation (alphabets and spaces only)
- Marks validation (0-100 range)
- Comprehensive error handling

### Initial Setup
- Project structure created
- Basic Python modules organized
- Git repository initialized
- README documentation

---

## Version History

- **v2.0.0** - Major update with MySQL database and profile management (Current)
- **v1.0.0** - Initial release with basic grade management features

---

## Upcoming Changes

See [Future Improvements](PRESENTATION.md#11-future-improvements) section in PRESENTATION.md for planned features.

---

## Contributors

- Maruf Shawkat Hossain (25013492) - Lead Developer
- Hasan Md Mahadi (25013422) - Developer & QA

---

## Academic Project

**Course:** Application of Programming Language-P  
**Institution:** Sejong University  
**Semester:** Fall 2024-2025  
**Instructor:** Sejan Mohammad Abrar Shakil
