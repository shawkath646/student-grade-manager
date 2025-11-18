from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List
import csv
import json
import os

from . import DEFAULT_GRADE_SCALE, DEFAULT_SUBJECTS
from .grading import compute_grade, validate_marks, validate_student_id, validate_student_name, validate_float_input
from .manager import StudentManager
from .models import Student
from .storage import load_students, save_students, DEFAULT_DATA_PATH


class StatisticsWindow(tk.Toplevel):
    """Window to display detailed statistics."""
    
    def __init__(self, parent: tk.Tk, manager: StudentManager) -> None:
        super().__init__(parent)
        self.title("Class Statistics")
        self.geometry("600x500")
        
        stats = manager.statistics()
        
        # Create scrollable text area
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_area = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Format statistics
        content = self._format_statistics(stats)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=5)
    
    def _format_statistics(self, stats: Dict[str, object]) -> str:
        """Format statistics for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("CLASS STATISTICS")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"Total Students: {stats['total_students']}")
        lines.append(f"Class Average: {stats['class_average']:.2f}%")
        lines.append(f"Pass Rate: {stats['pass_rate']:.1f}%")
        lines.append("")
        
        lines.append("Students by Grade:")
        grade_counts = stats.get('students_by_grade', {})
        for grade in sorted(grade_counts.keys(), reverse=True):
            count = grade_counts[grade]
            lines.append(f"  Grade {grade}: {count} student(s)")
        lines.append("")
        
        lines.append("Subject Averages:")
        subject_avgs = stats.get('subject_averages', {})
        for subject, avg in sorted(subject_avgs.items()):
            lines.append(f"  {subject}: {avg:.2f}%")
        lines.append("")
        
        lines.append("Top 3 Performers:")
        for i, (name, avg) in enumerate(stats.get('top_performers', []), 1):
            lines.append(f"  {i}. {name}: {avg:.2f}%")
        lines.append("")
        
        lines.append("Bottom 3 Performers:")
        for i, (name, avg) in enumerate(stats.get('bottom_performers', []), 1):
            lines.append(f"  {i}. {name}: {avg:.2f}%")
        lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


class GradeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Student Grade Management System")
        self.geometry("1100x750")

        self.manager = StudentManager(load_students())

        self._build_widgets()
        self._refresh_table()
        
        # Bind save on close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Configure tag colors for styling
        self._setup_table_tags()

    def _setup_table_tags(self) -> None:
        """Configure color tags for the table based on grades."""
        self.tree.tag_configure("grade_A", background="#90EE90")  # Light green
        self.tree.tag_configure("grade_B", background="#87CEEB")  # Sky blue
        self.tree.tag_configure("grade_C", background="#FFD700")  # Gold
        self.tree.tag_configure("grade_D", background="#FFA500")  # Orange
        self.tree.tag_configure("grade_F", background="#FFB6C1")  # Light pink

    def _on_closing(self) -> None:
        """Handle window closing - save data automatically."""
        try:
            save_students(self.manager.list_students())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
        self.destroy()

    def _build_widgets(self) -> None:
        # Menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self._on_save)
        file_menu.add_command(label="Reload", command=self._on_reload)
        file_menu.add_separator()
        file_menu.add_command(label="Import JSON", command=self._on_import_json)
        file_menu.add_command(label="Import CSV", command=self._on_import_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self._on_export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Statistics", command=self._show_statistics)
        
        form = ttk.LabelFrame(self, text="Student Details")
        form.pack(fill=tk.X, padx=10, pady=10)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.subject_vars: Dict[str, tk.StringVar] = {subj: tk.StringVar() for subj in DEFAULT_SUBJECTS}

        ttk.Label(form, text="ID").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        entry_id = ttk.Entry(form, textvariable=self.var_id, width=20)
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        entry_id.bind('<Return>', lambda e: self._on_add_update())

        ttk.Label(form, text="Name").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        entry_name = ttk.Entry(form, textvariable=self.var_name, width=30)
        entry_name.grid(row=0, column=3, padx=5, pady=5)
        entry_name.bind('<Return>', lambda e: self._focus_next())

        row = 1
        for i, subj in enumerate(DEFAULT_SUBJECTS):
            ttk.Label(form, text=subj).grid(row=row, column=0 + (i % 2) * 2, padx=5, pady=5, sticky=tk.W)
            entry_subj = ttk.Entry(form, textvariable=self.subject_vars[subj], width=10)
            entry_subj.grid(row=row, column=1 + (i % 2) * 2, padx=5, pady=5)
            if i % 2 == 1:
                row += 1

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btns, text="Add/Update", command=self._on_add_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Delete", command=self._on_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Clear Form", command=self._clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Save", command=self._on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Statistics", command=self._show_statistics).pack(side=tk.LEFT, padx=5)

        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        self.var_search = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self._on_search())
        ttk.Button(search_frame, text="Search", command=self._on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Clear", command=self._on_clear_search).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Sort by:").pack(side=tk.LEFT, padx=(20, 5))
        self.var_sort = tk.StringVar(value="Name")
        sort_combo = ttk.Combobox(search_frame, textvariable=self.var_sort, 
                                  values=["Name", "ID", "Average", "Total"], 
                                  state="readonly", width=12)
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self._refresh_table())

        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ("ID", "Name", "Total", "Average", "Grade", *DEFAULT_SUBJECTS)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col not in ("Name",) else 150)
        
        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        stats = ttk.Frame(self)
        stats.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_class_avg = ttk.Label(stats, text="Class Average: 0.00", font=("Arial", 9, "bold"))
        self.lbl_class_avg.pack(side=tk.LEFT, padx=5)
        self.lbl_top = ttk.Label(stats, text="Top Performers: -", font=("Arial", 9))
        self.lbl_top.pack(side=tk.LEFT, padx=15)
        self.lbl_total = ttk.Label(stats, text=f"Total Students: {self.manager.count_students()}", font=("Arial", 9))
        self.lbl_total.pack(side=tk.LEFT, padx=15)

    def _focus_next(self) -> None:
        """Focus next field."""
        if DEFAULT_SUBJECTS:
            self.focus_set()
            self.nametowidget(f".!labelframe.!entry2").focus()

    def _collect_student_from_form(self) -> Student:
        """Collect and validate student data from form."""
        try:
            # Validate ID
            sid = self.var_id.get().strip()
            validate_student_id(sid)
            
            # Validate name
            name = self.var_name.get().strip()
            validate_student_name(name)
            
            # Validate and collect marks
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
            
            # Validate all marks
            validate_marks(marks.values())
            
            return Student(student_id=sid, name=name, marks_by_subject=marks)
            
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")

    def _on_add_update(self) -> None:
        """Handle add/update button click."""
        try:
            student = self._collect_student_from_form()
            self.manager.add_or_update(student)
            self._refresh_table()
            # Auto-save
            try:
                save_students(self.manager.list_students())
            except Exception:
                pass  # Don't show error for auto-save
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
            # Auto-save
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
            
            # Validate file format
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
                    # Validate student data
                    validate_student_id(student.student_id)
                    validate_student_name(student.name)
                    validate_marks(student.marks_by_subject.values())
                    
                    # Check if student with same ID exists
                    existing = self.manager.get(student.student_id)
                    if existing:
                        # Update existing
                        self.manager.add_or_update(student)
                        imported_count += 1
                    else:
                        # Add new
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
                
                # Validate header
                expected_cols = ["ID", "Name"] + list(DEFAULT_SUBJECTS)
                if not all(col in reader.fieldnames for col in expected_cols):
                    missing = [col for col in expected_cols if col not in (reader.fieldnames or [])]
                    messagebox.showerror("Error", f"Invalid CSV format. Missing columns: {', '.join(missing)}")
                    return
                
                for idx, row in enumerate(reader, 1):
                    try:
                        # Extract ID and Name
                        sid = row.get("ID", "").strip()
                        name = row.get("Name", "").strip()
                        
                        validate_student_id(sid)
                        validate_student_name(name)
                        
                        # Extract marks
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
                # Write header
                writer.writerow(["ID", "Name", "Total", "Average", "Grade"] + list(DEFAULT_SUBJECTS))
                # Write data
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

    def _on_select(self, _event=None) -> None:
        """Handle table row selection."""
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        if not values:
            return
        # values: ID, Name, Total, Average, Grade, subjects...
        sid = values[0]
        student = self.manager.get(sid)
        if not student:
            return
        self.var_id.set(student.student_id)
        self.var_name.set(student.name)
        for subj in DEFAULT_SUBJECTS:
            self.subject_vars[subj].set(str(student.marks_by_subject.get(subj, 0)))

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
        
        # Sort students
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
            
            # Format values with better precision
            total_str = f"{s.total():.1f}"
            avg_str = f"{avg:.1f}"
            
            row = [s.student_id, s.name, total_str, avg_str, grade]
            row.extend(str(int(s.marks_by_subject.get(subj, 0))) for subj in DEFAULT_SUBJECTS)
            
            # Insert with grade-based color tag
            item = self.tree.insert("", tk.END, values=row, tags=(f"grade_{grade}",))
            
            # Apply tag-specific styling
            self.tree.set(item, "Grade", grade)

    def _update_stats(self) -> None:
        """Update statistics labels."""
        avg = self.manager.class_average()
        self.lbl_class_avg.config(text=f"Class Average: {avg:.2f}")
        top = self.manager.top_performers(3)
        top_txt = ", ".join(f"{s.name} ({s.average():.1f})" for s in top) if top else "-"
        self.lbl_top.config(text=f"Top Performers: {top_txt}")
        self.lbl_total.config(text=f"Total Students: {self.manager.count_students()}")
