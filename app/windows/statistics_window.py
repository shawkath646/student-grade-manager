from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

class StatisticsWindow(tk.Toplevel):
    
    def __init__(self, parent: tk.Tk, manager) -> None:
        super().__init__(parent)
        self.title("Class Statistics")
        self.geometry("700x600")
        self.configure(bg='#f0f0f0')
        
        stats = manager.statistics()
        
        header = tk.Frame(self, bg='#2c3e50', height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="📊 Class Statistics", font=('Segoe UI', 16, 'bold'), 
                bg='#2c3e50', fg='white', pady=12).pack()
        
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        text_area = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 11), bg='#ffffff', 
                           relief=tk.FLAT, borderwidth=0, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        content = self._format_statistics(stats)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="✖️ Close", command=self.destroy, style='Action.TButton').pack()
    
    def _format_statistics(self, stats: Dict[str, object]) -> str:
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
