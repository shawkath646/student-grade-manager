"""
Entry point for the Student Grade Manager application.
This file is used by PyInstaller to create the executable.
"""
import sys
import os

# Add the project root to the Python path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# Now import and run the application
from app.gui import GradeApp

def main():
    app = GradeApp()
    app.mainloop()

if __name__ == "__main__":
    main()
