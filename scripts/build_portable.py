"""
Build script for creating a portable executable of Student Grade Manager.
This script automates the process of building a standalone .exe file.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    print("Checking for PyInstaller...")
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

def clean_build_folders():
    """Remove previous build artifacts."""
    print("\nCleaning previous build artifacts...")
    folders_to_remove = ['build', 'dist', '__pycache__']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Removed {folder}/")
    
                                              
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'build_exe.spec':
            spec_file.unlink()

def build_executable():
    """Build the executable using PyInstaller."""
    print("\nBuilding portable executable...")
    print("This may take several minutes...\n")
    
                                        
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--clean", "scripts/build_exe.spec"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Build completed successfully!")
        return True
    else:
        print("✗ Build failed!")
        print("\nError output:")
        print(result.stderr)
        return False

def create_portable_package():
    """Create a portable package with the executable and necessary files."""
    print("\nCreating portable package...")
    
    portable_dir = Path("dist/StudentGradeManager_Portable")
    portable_dir.mkdir(parents=True, exist_ok=True)
    
                         
    exe_path = Path("dist/StudentGradeManager.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, portable_dir / "StudentGradeManager.exe")
        print("✓ Copied executable")
    
                                                     
    data_src = Path("data")
    if data_src.exists():
        data_dst = portable_dir / "data"
        if data_dst.exists():
            shutil.rmtree(data_dst)
        shutil.copytree(data_src, data_dst)
        print("✓ Copied data folder")
    
                                     
    assets_src = Path("assets")
    if assets_src.exists():
        assets_dst = portable_dir / "assets"
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
        print("✓ Copied assets folder")
    
                                        
    readme_content = """# Student Grade Manager - Portable Version

## How to Use

1. Simply run StudentGradeManager.exe to start the application
2. No installation or additional dependencies required
3. The application will use the 'data' folder in this directory to store student information

## Database Configuration

By default, this application uses JSON file storage. If you want to use MySQL:
1. Make sure MySQL server is installed and running on your system
2. Configure the database connection in the application settings

## System Requirements

- Windows 7 or later
- No Python installation required
- No additional dependencies needed

## Notes

- All student data is stored in the 'data' folder
- Keep this folder in the same directory as the executable
- You can copy this entire folder to any Windows PC to run the application

For more information, visit: https://github.com/shawkath646/student-grade-manager
"""
    
    with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✓ Created README.txt")
    
                               
    if Path("LICENSE").exists():
        shutil.copy2("LICENSE", portable_dir / "LICENSE.txt")
        print("✓ Copied LICENSE")
    
    print(f"\n✓ Portable package created at: {portable_dir.absolute()}")
    return portable_dir

def main():
    """Main build process."""
    print("=" * 60)
    print("Student Grade Manager - Portable Executable Builder")
    print("=" * 60)
    
                                 
    install_pyinstaller()
    
                                   
    clean_build_folders()
    
                              
    if not build_executable():
        print("\nBuild process failed. Please check the errors above.")
        sys.exit(1)
    
                                     
    portable_dir = create_portable_package()
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nYour portable application is ready at:")
    print(f"  {portable_dir.absolute()}")
    print("\nYou can now:")
    print("  1. Run StudentGradeManager.exe from that folder")
    print("  2. Copy the entire folder to any Windows PC")
    print("  3. No installation or dependencies required!")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
