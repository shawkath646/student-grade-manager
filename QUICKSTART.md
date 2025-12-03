# Quick Start Guide

## Running the Application

### For End Users (No Programming Required)

**Download and Run the Portable Executable:**

1. Download the `StudentGradeManager_Portable` folder
2. No installation needed - just run `StudentGradeManager.exe`
3. Works on any Windows PC without Python

### For Developers

**1. Clone and Setup:**
```bash
git clone https://github.com/shawkath646/student-grade-manager.git
cd student-grade-manager
pip install -r requirements.txt
```

**2. Run in Development Mode:**
```bash
python run.py
```

**3. Build Portable Executable:**
```bash
python scripts/build_portable.py
```

## Project Organization

- `/app` - Main application code
- `/scripts` - Build and deployment scripts
- `/data` - Student records and images
- `/assets` - Static resources

## Key Files

- `run.py` - Quick launcher for development
- `launch.bat` - Windows batch launcher
- `requirements.txt` - Python dependencies
- `setup.py` - Package configuration

For detailed documentation, see [README.md](README.md)
