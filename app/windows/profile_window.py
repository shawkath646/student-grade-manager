from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict
import os
from PIL import Image, ImageTk

class ProfileWindow(tk.Toplevel):
    
    def __init__(self, parent: tk.Tk, student_id: str, student_name: str, profile_data: Dict) -> None:
        super().__init__(parent)
        self.title(f"Student Profile - {student_name}")
        self.geometry("1000x900")
        self.configure(bg='#f0f0f0')
        self.resizable(True, True)
        self.minsize(700, 500)
        
        self.transient(parent)
        self.grab_set()
        
        self.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.bind('<Escape>', lambda e: self.exit_fullscreen())
        self._is_fullscreen = False
        
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"👤 {student_name}", font=('Segoe UI', 20, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=(15, 5))
        
        canvas = tk.Canvas(self, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        container = ttk.Frame(scrollable_frame)
        container.pack(fill=tk.BOTH, expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        left_column = ttk.Frame(container)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        right_column = ttk.Frame(container)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        photo_frame = tk.Frame(left_column, bg='white', relief=tk.SOLID, bd=1)
        photo_frame.pack(pady=(0, 15))
        
        photo_path = profile_data.get('photo_path', '')
        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img = img.resize((180, 180), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                photo_label = tk.Label(photo_frame, image=photo, bg='white')
                photo_label.image = photo
                photo_label.pack(padx=10, pady=10)
            except Exception as e:
                tk.Label(photo_frame, text="📷 No Photo", font=('Segoe UI', 11), 
                        fg='#7f8c8d', bg='white', padx=20, pady=20).pack()
        else:
            tk.Label(photo_frame, text="📷 No Photo", font=('Segoe UI', 11), 
                    fg='#7f8c8d', bg='white', padx=20, pady=20).pack()
        
        info_card = self._create_info_card(left_column, "📋 Personal Information", [
            ("Name", student_name),
            ("Date of Birth", profile_data.get('date_of_birth', 'N/A')),
            ("Gender", profile_data.get('gender', 'N/A')),
            ("Blood Group", profile_data.get('blood_group', 'N/A')),
            ("Religion", profile_data.get('religion', 'N/A')),
            ("Nationality", profile_data.get('nationality', 'N/A')),
        ])
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        contact_card = self._create_info_card(left_column, "📞 Contact Details", [
            ("Phone", profile_data.get('phone', 'N/A')),
            ("Email", profile_data.get('email', 'N/A')),
            ("Address", profile_data.get('address', 'N/A')),
            ("Emergency", profile_data.get('emergency_contact', 'N/A')),
        ])
        contact_card.pack(fill=tk.X)
        
        academic_card = self._create_info_card(right_column, "🎓 Academic Information", [
            ("Session", profile_data.get('session', 'N/A')),
            ("Department", profile_data.get('department', 'N/A')),
            ("Semester", profile_data.get('semester', 'N/A')),
            ("Previous CGPA", f"{profile_data.get('previous_cgpa', 0.0):.2f}" if profile_data.get('previous_cgpa') else 'N/A'),
        ])
        academic_card.pack(fill=tk.X, pady=(0, 15))
        
        father_card = self._create_info_card(right_column, "👨 Father's Information", [
            ("Name", profile_data.get('father_name', 'N/A')),
            ("Occupation", profile_data.get('father_occupation', 'N/A')),
            ("Phone", profile_data.get('father_phone', 'N/A')),
        ])
        father_card.pack(fill=tk.X, pady=(0, 15))
        
        mother_card = self._create_info_card(right_column, "👩 Mother's Information", [
            ("Name", profile_data.get('mother_name', 'N/A')),
            ("Occupation", profile_data.get('mother_occupation', 'N/A')),
            ("Phone", profile_data.get('mother_phone', 'N/A')),
        ])
        mother_card.pack(fill=tk.X)
    
    def toggle_fullscreen(self):
        self._is_fullscreen = not self._is_fullscreen
        self.attributes('-fullscreen', self._is_fullscreen)
        return 'break'
    
    def exit_fullscreen(self):
        if self._is_fullscreen:
            self._is_fullscreen = False
            self.attributes('-fullscreen', False)
        return 'break'
    
    def _create_info_card(self, parent, title: str, data: list) -> tk.Frame:
        card = tk.Frame(parent, bg='white', relief=tk.SOLID, bd=1)
        
        title_frame = tk.Frame(card, bg='#3498db', height=35)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text=title, font=('Segoe UI', 11, 'bold'), 
                bg='#3498db', fg='white').pack(side=tk.LEFT, padx=12, pady=8)
        
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        for label, value in data:
            row = tk.Frame(content, bg='white')
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(row, text=f"{label}:", font=('Segoe UI', 9, 'bold'), 
                    bg='white', fg='#5d6d7e', width=14, anchor='w').pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=('Segoe UI', 9), 
                    bg='white', fg='#2c3e50', anchor='w', wraplength=250).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        return card
