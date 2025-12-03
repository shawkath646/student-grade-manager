# Build Scripts

This directory contains scripts for building and packaging the Student Grade Manager application.

## Files

### build_portable.py
Main build script for creating a portable executable of the application.

**Usage:**
```bash
python scripts/build_portable.py
```

**What it does:**
1. Installs PyInstaller if not already installed
2. Cleans previous build artifacts
3. Builds a standalone executable using PyInstaller
4. Creates a portable package with all necessary files
5. Outputs to `dist/StudentGradeManager_Portable/`

**Output:**
- `StudentGradeManager.exe` - Standalone executable (no Python or dependencies required)
- Complete portable folder that can be copied to any Windows PC

### build_exe.spec
PyInstaller specification file that defines how the executable should be built.

**Configuration:**
- Entry point: `run_app.py`
- Includes: data folder, assets folder
- Hidden imports: MySQL, PIL, matplotlib, tkinter
- Console mode: Disabled (GUI application)
- Compression: UPX enabled

### run_app.py
Entry point script for the application when building executables.

**Features:**
- Handles both frozen (executable) and script modes
- Sets up proper Python path for imports
- Uses absolute imports instead of relative imports
- Compatible with PyInstaller

## Building Process

1. **Clean Build:**
   ```bash
   python scripts/build_portable.py
   ```
   This will automatically clean previous builds and create a fresh executable.

2. **Manual Build (Advanced):**
   ```bash
   pyinstaller --clean scripts/build_exe.spec
   ```

## Output Structure

```
dist/StudentGradeManager_Portable/
├── StudentGradeManager.exe    # Main executable
├── data/                      # Student data
├── assets/                    # Application assets
├── README.txt                 # User instructions
└── LICENSE.txt               # License file
```

## Requirements

- Python 3.10+
- PyInstaller (auto-installed by build script)
- All dependencies from requirements.txt

## Notes

- The executable is self-contained and includes Python runtime
- Expected size: 40-80 MB (includes all dependencies)
- No installation required on target systems
- Compatible with Windows 7 and later
