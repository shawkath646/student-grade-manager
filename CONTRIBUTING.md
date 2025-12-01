# Contributing to Student Grade Management System

Thank you for considering contributing to our project! This document provides guidelines for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project is an academic project for Sejong University. We expect all contributors to:

- Be respectful and professional
- Provide constructive feedback
- Focus on learning and improvement
- Give credit where credit is due

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, MySQL version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear description** of the feature
- **Use case** - why is this needed?
- **Possible implementation** approach
- **Alternatives considered**

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

---

## Development Setup

### Prerequisites

- Python 3.13 or higher
- MySQL 8.0 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/shawkath646/student-grade-manager.git
cd student-grade-manager

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.db import init_database; init_database()"

# Run the application
python -m app.main
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Indentation:** 4 spaces (no tabs)
- **Line length:** Maximum 100 characters
- **Imports:** Group in order - standard library, third-party, local
- **Naming:**
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_CASE`

### Type Hints

Use type hints for all function signatures:

```python
def calculate_grade(average: float) -> str:
    """Determine letter grade based on average."""
    pass
```

### Documentation

- Add docstrings to all functions and classes
- Use clear, descriptive variable names
- Comment complex logic

### Code Example

```python
from typing import Dict, Tuple

def calculate_total_average(marks: Dict[str, int]) -> Tuple[int, float]:
    """
    Calculate total and average from marks dictionary.
    
    Args:
        marks: Dictionary with subject names as keys and marks as values
        
    Returns:
        Tuple containing (total, average)
    """
    total = sum(marks.values())
    average = total / len(marks) if marks else 0.0
    return total, round(average, 2)
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, no logic change)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

### Examples

```
feat(profile): add fullscreen support to profile window

- Added F11 keyboard shortcut for fullscreen toggle
- Added Escape key to exit fullscreen
- Updated profile window to support resizing

Closes #123
```

```
fix(db): resolve connection pool exhaustion issue

- Implemented proper connection cleanup in finally blocks
- Added connection timeout configuration
- Fixed memory leak in get_connection()
```

---

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add code comments and docstrings
   - Update PRESENTATION.md if adding major features

2. **Test Your Changes**
   - Test all affected functionality
   - Verify database operations
   - Check for UI issues

3. **Create Pull Request**
   - Use clear, descriptive title
   - Reference related issues
   - Describe changes in detail
   - Add screenshots for UI changes

4. **Review Process**
   - Address review comments
   - Keep discussion focused
   - Be open to feedback

---

## Testing Guidelines

### Manual Testing

Currently, we use manual testing. When testing:

- Test with sample data (`students.sample.json`)
- Test edge cases (empty input, invalid data)
- Test all CRUD operations
- Test import/export functionality
- Test profile window features

### Future: Automated Testing

We plan to add:
- Unit tests with pytest
- Integration tests for database
- GUI tests

---

## Questions?

If you have questions about contributing:

- Open an issue with the "question" label
- Contact: shawkath646@gmail.com

---

## Academic Project Note

This is an academic project for:
- **Course:** Application of Programming Language-P
- **Institution:** Sejong University
- **Semester:** Fall 2024-2025
- **Instructor:** Sejan Mohammad Abrar Shakil

Contributors will be acknowledged in project documentation.

---

**Thank you for contributing to our learning journey! 🎓**
