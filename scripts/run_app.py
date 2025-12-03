"""
Entry point for the Student Grade Manager application.
This file is used by PyInstaller to create the executable.
"""
import sys
import os

                                         
if getattr(sys, 'frozen', False):
                                    
    application_path = sys._MEIPASS
else:
                       
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

                                    
from app.gui import GradeApp

def main():
    app = GradeApp()
    app.mainloop()

if __name__ == "__main__":
    main()
