from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List
import csv
import json
import sys
import ctypes
import os
from PIL import Image, ImageTk

from . import DEFAULT_GRADE_SCALE, DEFAULT_SUBJECTS
from .grading import compute_grade, validate_marks, validate_student_id, validate_student_name, validate_float_input
from .manager import StudentManager
from .models import Student
from .storage import load_students, save_students
from .windows import StatisticsWindow, ProfileWindow


if sys.platform == 'win32':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class GradeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Student Grade Management System")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TLabelframe', background='#f0f0f0', font=('Segoe UI', 10, 'bold'))
        style.configure('TLabelframe.Label', background='#f0f0f0', foreground='#2c3e50', font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 9), padding=6)
        style.configure('TEntry', fieldbackground='white', font=('Segoe UI', 10))
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#34495e', foreground='white')
        style.map('Treeview.Heading', background=[('active', "#326fab")])
        
        style.configure('Action.TButton', font=('Segoe UI', 9, 'bold'), padding=8)
        style.map('Action.TButton', background=[('active', '#3498db')], foreground=[('active', 'white')])

        self.manager = StudentManager(load_students())
        self.profile_window = None
        self._build_widgets()
        self._refresh_table()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._setup_table_tags()

    def _setup_table_tags(self) -> None:
        self.tree.tag_configure("grade_A", background="#d4edda", foreground="#155724")
        self.tree.tag_configure("grade_B", background="#d1ecf1", foreground="#0c5460")
        self.tree.tag_configure("grade_C", background="#fff3cd", foreground="#856404")
        self.tree.tag_configure("grade_D", background="#f8d7da", foreground="#721c24")
        self.tree.tag_configure("grade_F", background="#f5c6cb", foreground="#721c24")

    def _on_closing(self) -> None:
        try:
            save_students(self.manager.list_students())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
        self.destroy()

    def _build_widgets(self) -> None:
        menubar = tk.Menu(self, bg='#34495e', fg='white', font=('Segoe UI', 9))
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, font=('Segoe UI', 9))
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="💾 Save", command=self._on_save)
        file_menu.add_command(label="🔄 Reload", command=self._on_reload)
        file_menu.add_separator()
        file_menu.add_command(label="📥 Import JSON", command=self._on_import_json)
        file_menu.add_command(label="📥 Import CSV", command=self._on_import_csv)
        file_menu.add_separator()
        file_menu.add_command(label="📤 Export to CSV", command=self._on_export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self._on_closing)
        
        tools_menu = tk.Menu(menubar, tearoff=0, font=('Segoe UI', 9))
        menubar.add_cascade(label="🛠️ Tools", menu=tools_menu)
        tools_menu.add_command(label="📊 Statistics", command=self._show_statistics)
        
        header = tk.Frame(self, bg='#2c3e50', height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        self.logo_photo = None
                                                           
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sejong_logo.png')

        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                                                            
                logo_img.thumbnail((150, 300), Image.Resampling.LANCZOS)

                                                        
                padding = 4
                card_width = logo_img.width + padding * 2
                card_height = logo_img.height + padding * 2

                                 
                card_bg = Image.new("RGBA", (card_width, card_height), (0, 0, 0, 0))

                                             
                from PIL import ImageDraw
                radius = 8
                mask = Image.new("L", (card_width, card_height), 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle(
                    [(0, 0), (card_width, card_height)],
                    radius=radius,
                    fill=255,
                )

                                  
                card_color = (245, 247, 250, 210)
                card_color_img = Image.new("RGBA", (card_width, card_height), card_color)
                card_bg = Image.composite(card_color_img, card_bg, mask)

                offset = ((card_width - logo_img.width) // 2, (card_height - logo_img.height) // 2)
                card_bg.paste(logo_img, offset, logo_img if logo_img.mode == 'RGBA' else None)

                self.logo_photo = ImageTk.PhotoImage(card_bg)

                                                                                               
                logo_container = tk.Frame(
                    header,
                    bg="#2c3e50",
                    highlightthickness=0,
                )
                logo_container.pack(side=tk.RIGHT, padx=24, pady=6)

                logo_label = tk.Label(
                    logo_container,
                    image=self.logo_photo,
                    bg="#2c3e50",
                    bd=0,
                    relief=tk.FLAT,
                )
                logo_label.pack()
            except Exception:
                logo_label = tk.Label(
                    header,
                    text="SEJONG",
                    font=('Segoe UI', 10, 'bold'),
                    bg='#2c3e50',
                    fg='white',
                    padx=10,
                    pady=5,
                    relief=tk.RAISED,
                    borderwidth=2,
                )
                logo_label.pack(side=tk.RIGHT, padx=20, pady=5)
        else:
            logo_label = tk.Label(
                header,
                text="SEJONG",
                font=('Segoe UI', 10, 'bold'),
                bg='#2c3e50',
                fg='white',
                padx=10,
                pady=5,
                relief=tk.RAISED,
                borderwidth=2,
            )
            logo_label.pack(side=tk.RIGHT, padx=20, pady=5)
        
        title_label = tk.Label(header, text="🎓 Student Grade Management", font=('Segoe UI', 18, 'bold'), 
                               bg='#2c3e50', fg='white', pady=15)
        title_label.pack(side=tk.LEFT, padx=20)
        
        form = ttk.LabelFrame(self, text="  📝 Student Information  ", padding=15)
        form.pack(fill=tk.X, padx=15, pady=15)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.subject_vars: Dict[str, tk.StringVar] = {subj: tk.StringVar() for subj in DEFAULT_SUBJECTS}

        ttk.Label(form, text="Student ID:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)
        entry_id = ttk.Entry(form, textvariable=self.var_id, width=22, font=('Segoe UI', 10))
        entry_id.grid(row=0, column=1, padx=8, pady=8)
        entry_id.bind('<Return>', lambda e: self._on_add_update())

        ttk.Label(form, text="Name:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=2, padx=8, pady=8, sticky=tk.W)
        entry_name = ttk.Entry(form, textvariable=self.var_name, width=35, font=('Segoe UI', 10))
        entry_name.grid(row=0, column=3, padx=8, pady=8)
        entry_name.bind('<Return>', lambda e: self._focus_next())

        row = 1
        for i, subj in enumerate(DEFAULT_SUBJECTS):
            ttk.Label(form, text=f"{subj}:", font=('Segoe UI', 10)).grid(row=row, column=0 + (i % 2) * 2, padx=8, pady=8, sticky=tk.W)
            entry_subj = ttk.Entry(form, textvariable=self.subject_vars[subj], width=12, font=('Segoe UI', 10))
            entry_subj.grid(row=row, column=1 + (i % 2) * 2, padx=8, pady=8)
            if i % 2 == 1:
                row += 1

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        btn_add = ttk.Button(btn_frame, text="➕ Add/Update", command=self._on_add_update, style='Action.TButton')
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_delete = ttk.Button(btn_frame, text="🗑️ Delete", command=self._on_delete)
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        btn_clear = ttk.Button(btn_frame, text="🔄 Clear Form", command=self._clear_form)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_save = ttk.Button(btn_frame, text="💾 Save", command=self._on_save)
        btn_save.pack(side=tk.LEFT, padx=5)
        
        btn_stats = ttk.Button(btn_frame, text="📊 Statistics", command=self._show_statistics)
        btn_stats.pack(side=tk.LEFT, padx=5)

        search_frame = ttk.LabelFrame(self, text="  🔍 Search & Filter  ", padding=10)
        search_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.var_search = tk.StringVar()
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=30, font=('Segoe UI', 10))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self._on_search())
        
        ttk.Button(search_frame, text="🔍 Search", command=self._on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="✖️ Clear", command=self._on_clear_search).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Sort by:").pack(side=tk.LEFT, padx=(20, 5))
        self.var_sort = tk.StringVar(value="Name")
        sort_combo = ttk.Combobox(search_frame, textvariable=self.var_sort, 
                                  values=["Name", "ID", "Average", "Total"], 
                                  state="readonly", width=12, font=('Segoe UI', 10))
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self._refresh_table())

        tree_frame = ttk.LabelFrame(self, text="  📋 Student Records  ", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        columns = ("ID", "Name", "Profile", "Total", "Average", "Grade", *DEFAULT_SUBJECTS)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Profile":
                self.tree.column(col, width=100, anchor=tk.CENTER)
            elif col == "Name":
                self.tree.column(col, width=180)
            else:
                self.tree.column(col, width=100)
        
        self.scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self._on_y_scroll, xscrollcommand=self._on_x_scroll)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.scrollbar_y.grid_remove()
        self.scrollbar_x.grid_remove()
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Button-1>", self._on_tree_click)

        stats_frame = tk.Frame(self, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.lbl_total = tk.Label(stats_frame, text=f"👥 Total Students: {self.manager.count_students()}", 
                                  font=("Segoe UI", 10, "bold"), bg='#ecf0f1', fg='#2c3e50')
        self.lbl_total.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.lbl_class_avg = tk.Label(stats_frame, text="📈 Class Average: 0.00%", 
                                      font=("Segoe UI", 10, "bold"), bg='#ecf0f1', fg='#27ae60')
        self.lbl_class_avg.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.lbl_top = tk.Label(stats_frame, text="🏆 Top Performers: -", 
                               font=("Segoe UI", 10), bg='#ecf0f1', fg='#34495e')
        self.lbl_top.pack(side=tk.LEFT, padx=15, pady=10)
        
        credit_label = tk.Label(stats_frame, text="Made by Maruf Shawkat Hossain and MD Mahadi Hasan", 
                               font=('Segoe UI', 9, 'italic'), bg='#ecf0f1', fg='#7f8c8d')
        credit_label.pack(side=tk.RIGHT, padx=15, pady=10)

    def _focus_next(self) -> None:
        """Focus next field."""
        if DEFAULT_SUBJECTS:
            self.focus_set()
            self.nametowidget(f".!labelframe.!entry2").focus()

    def _collect_student_from_form(self) -> Student:
        """Collect and validate student data from form."""
        try:
            sid = self.var_id.get().strip()
            validate_student_id(sid)
            
            name = self.var_name.get().strip()
            validate_student_name(name)
            
            marks = {}
            for subj, var in self.subject_vars.items():
                txt = var.get().strip()
                if txt:
                    try:
                        marks[subj] = validate_float_input(txt, f"{subj} marks")
                    except ValueError as e:
                        raise ValueError(f"Invalid {subj} marks: {str(e)}")
                else:
                    marks[subj] = 0.0
            
                                
            validate_marks(marks.values())
            
            return Student(student_id=sid, name=name, marks_by_subject=marks)
            
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")

    def _on_add_update(self) -> None:
        try:
            student = self._collect_student_from_form()
            existing = self.manager.get(student.student_id)
            self.manager.add_or_update(student)
            self._refresh_table()
            try:
                save_students(self.manager.list_students())
            except Exception:
                pass
            
            if existing:
                messagebox.showinfo("✅ Success", f"Student '{student.name}' updated successfully!")
            else:
                messagebox.showinfo("✅ Success", f"Student '{student.name}' added successfully!")
            
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_delete(self) -> None:
        """Handle delete button click."""
        sid = self.var_id.get().strip()
        if not sid:
            messagebox.showwarning("Warning", "Enter an ID to delete.")
            return
        try:
            validate_student_id(sid)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        if self.manager.delete(sid):
            self._refresh_table()
            self._clear_form()
                       
            try:
                save_students(self.manager.list_students())
            except Exception:
                pass
            messagebox.showinfo("Success", "Student deleted successfully.")
        else:
            messagebox.showinfo("Info", "Student not found.")

    def _on_save(self) -> None:
        """Handle save button click."""
        try:
            save_students(self.manager.list_students())
            messagebox.showinfo("Saved", "Students saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def _on_reload(self) -> None:
        """Handle reload button click."""
        try:
            self.manager = StudentManager(load_students())
            self._refresh_table()
            self._clear_form()
            messagebox.showinfo("Reloaded", "Data reloaded from file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload: {str(e)}")

    def _on_search(self) -> None:
        """Handle search button click."""
        q = self.var_search.get().strip()
        if not q:
            self._refresh_table()
            return
        self._populate_table(self.manager.search(q))
        self._update_stats()

    def _on_clear_search(self) -> None:
        """Handle clear search button click."""
        self.var_search.set("")
        self._refresh_table()

    def _on_import_json(self) -> None:
        """Import students from JSON file."""
        try:
            filename = filedialog.askopenfilename(
                title="Select JSON File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not filename:
                return
            
                                  
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                messagebox.showerror("Error", "Invalid JSON format: File should contain a list of students.")
                return
            
            imported_count = 0
            skipped_count = 0
            errors = []
            
            for idx, item in enumerate(data, 1):
                try:
                    student = Student.from_dict(item)
                                           
                    validate_student_id(student.student_id)
                    validate_student_name(student.name)
                    validate_marks(student.marks_by_subject.values())
                    
                                                          
                    existing = self.manager.get(student.student_id)
                    if existing:
                                         
                        self.manager.add_or_update(student)
                        imported_count += 1
                    else:
                                 
                        self.manager.add_or_update(student)
                        imported_count += 1
                        
                except Exception as e:
                    skipped_count += 1
                    errors.append(f"Row {idx}: {str(e)}")
            
            if errors:
                msg = f"Imported {imported_count} student(s).\nSkipped {skipped_count} record(s) with errors."
                if len(errors) <= 5:
                    msg += "\n\nErrors:\n" + "\n".join(errors)
                else:
                    msg += f"\n\n{len(errors)} errors occurred (showing first 5):\n" + "\n".join(errors[:5])
                messagebox.showwarning("Partial Import", msg)
            else:
                messagebox.showinfo("Success", f"Successfully imported {imported_count} student(s).")
            
            self._refresh_table()
            try:
                save_students(self.manager.list_students())
            except Exception:
                pass
                
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON file: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {str(e)}")

    def _on_import_csv(self) -> None:
        """Import students from CSV file."""
        try:
            filename = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not filename:
                return
            
            imported_count = 0
            skipped_count = 0
            errors = []
            
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                                 
                expected_cols = ["ID", "Name"] + list(DEFAULT_SUBJECTS)
                if not all(col in reader.fieldnames for col in expected_cols):
                    missing = [col for col in expected_cols if col not in (reader.fieldnames or [])]
                    messagebox.showerror("Error", f"Invalid CSV format. Missing columns: {', '.join(missing)}")
                    return
                
                for idx, row in enumerate(reader, 1):
                    try:
                                             
                        sid = row.get("ID", "").strip()
                        name = row.get("Name", "").strip()
                        
                        validate_student_id(sid)
                        validate_student_name(name)
                        
                                       
                        marks = {}
                        for subj in DEFAULT_SUBJECTS:
                            mark_str = row.get(subj, "0").strip()
                            marks[subj] = validate_float_input(mark_str, f"{subj} marks") if mark_str else 0.0
                        
                        validate_marks(marks.values())
                        
                        student = Student(student_id=sid, name=name, marks_by_subject=marks)
                        self.manager.add_or_update(student)
                        imported_count += 1
                        
                    except Exception as e:
                        skipped_count += 1
                        errors.append(f"Row {idx}: {str(e)}")
            
            if errors:
                msg = f"Imported {imported_count} student(s).\nSkipped {skipped_count} record(s) with errors."
                if len(errors) <= 5:
                    msg += "\n\nErrors:\n" + "\n".join(errors)
                else:
                    msg += f"\n\n{len(errors)} errors occurred (showing first 5):\n" + "\n".join(errors[:5])
                messagebox.showwarning("Partial Import", msg)
            else:
                messagebox.showinfo("Success", f"Successfully imported {imported_count} student(s).")
            
            self._refresh_table()
            try:
                save_students(self.manager.list_students())
            except Exception:
                pass
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")

    def _on_export_csv(self) -> None:
        """Export data to CSV file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not filename:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                              
                writer.writerow(["ID", "Name", "Total", "Average", "Grade"] + list(DEFAULT_SUBJECTS))
                            
                for student in self.manager.list_students():
                    avg = student.average()
                    grade = compute_grade(avg, DEFAULT_GRADE_SCALE)
                    row = [
                        student.student_id,
                        student.name,
                        f"{student.total():.2f}",
                        f"{avg:.2f}",
                        grade
                    ]
                    row.extend(str(student.marks_by_subject.get(subj, 0)) for subj in DEFAULT_SUBJECTS)
                    writer.writerow(row)
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def _show_statistics(self) -> None:
        """Show detailed statistics window."""
        if self.manager.count_students() == 0:
            messagebox.showinfo("Info", "No students to display statistics.")
            return
        StatisticsWindow(self, self.manager)
    
    def _show_profile(self, student_id: str) -> None:
        """Show student profile window."""
        from .db import get_profile
        
        if self.profile_window and self.profile_window.winfo_exists():
            self.profile_window.lift()
            messagebox.showinfo("Info", "A profile window is already open. Please close it first.")
            return
        
        student = self.manager.get(student_id)
        if not student:
            messagebox.showerror("Error", f"Student {student_id} not found.")
            return
        
        profile_data = get_profile(student_id)
        if not profile_data:
            messagebox.showwarning("No Profile", f"No profile data found for {student.name}.")
            return
        
        self.profile_window = ProfileWindow(self, student_id, student.name, profile_data)
        self.profile_window.protocol("WM_DELETE_WINDOW", self._on_profile_close)
    
    def _on_profile_close(self) -> None:
        """Handle profile window close."""
        if self.profile_window:
            self.profile_window.destroy()
            self.profile_window = None

    def _on_select(self, _event=None) -> None:
        """Handle table row selection."""
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        if not values:
            return
        sid = values[0]
        student = self.manager.get(sid)
        if not student:
            return
        self.var_id.set(student.student_id)
        self.var_name.set(student.name)
        for subj in DEFAULT_SUBJECTS:
            self.subject_vars[subj].set(str(student.marks_by_subject.get(subj, 0)))
    
    def _on_tree_click(self, event) -> None:
        """Handle click on tree to show profile."""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        
        if not item:
            return
        
                                                                   
        if column == "#3":
            values = self.tree.item(item, "values")
            if values:
                student_id = values[0]
                self._show_profile(student_id)
    
    def _on_y_scroll(self, first, last):
        """Auto-hide/show vertical scrollbar."""
        first, last = float(first), float(last)
        if first <= 0.0 and last >= 1.0:
            self.scrollbar_y.grid_remove()
        else:
            self.scrollbar_y.grid()
        self.scrollbar_y.set(first, last)
    
    def _on_x_scroll(self, first, last):
        """Auto-hide/show horizontal scrollbar."""
        first, last = float(first), float(last)
        if first <= 0.0 and last >= 1.0:
            self.scrollbar_x.grid_remove()
        else:
            self.scrollbar_x.grid()
        self.scrollbar_x.set(first, last)

    def _clear_form(self) -> None:
        """Clear all form fields."""
        self.var_id.set("")
        self.var_name.set("")
        for var in self.subject_vars.values():
            var.set("")

    def _refresh_table(self) -> None:
        """Refresh table with current data."""
        self._populate_table(self.manager.list_students())
        self._update_stats()

    def _populate_table(self, students: List[Student]) -> None:
        """Populate table with student data."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
                       
        sort_by = self.var_sort.get()
        if sort_by == "Name":
            students.sort(key=lambda s: s.name)
        elif sort_by == "ID":
            students.sort(key=lambda s: s.student_id)
        elif sort_by == "Average":
            students.sort(key=lambda s: s.average(), reverse=True)
        elif sort_by == "Total":
            students.sort(key=lambda s: s.total(), reverse=True)
        
        for s in students:
            avg = s.average()
            grade = compute_grade(avg, DEFAULT_GRADE_SCALE)
            
            total_str = f"{s.total():.1f}"
            avg_str = f"{avg:.1f}"
            
            row = [s.student_id, s.name, "View", total_str, avg_str, grade]
            row.extend(str(int(s.marks_by_subject.get(subj, 0))) for subj in DEFAULT_SUBJECTS)
            
            item = self.tree.insert("", tk.END, values=row, tags=(f"grade_{grade}",))
            
            self.tree.set(item, "Grade", grade)

    def _update_stats(self) -> None:
        avg = self.manager.class_average()
        self.lbl_class_avg.config(text=f"📈 Class Average: {avg:.2f}%")
        top = self.manager.top_performers(3)
        top_txt = ", ".join(f"{s.name} ({s.average():.1f}%)" for s in top) if top else "-"
        self.lbl_top.config(text=f"🏆 Top Performers: {top_txt}")
        self.lbl_total.config(text=f"👥 Total Students: {self.manager.count_students()}")
