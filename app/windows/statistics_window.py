from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatisticsWindow(tk.Toplevel):
    
    def __init__(self, parent: tk.Tk, manager) -> None:
        super().__init__(parent)
        self.title("Class Statistics")
        self.geometry("1000x800")
        self.configure(bg='#f0f0f0')
        
        stats = manager.statistics()
        
        header = tk.Frame(self, bg='#2c3e50', height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="📊 Class Statistics", font=('Segoe UI', 16, 'bold'), 
                bg='#2c3e50', fg='white', pady=12).pack()
        
                                   
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
                       
        self._create_graphs(main_container, stats)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="✖️ Close", command=self.destroy).pack()
    
    def _create_graphs(self, parent: ttk.Frame, stats: Dict) -> None:
        """Create visualization graphs."""
                                     
        fig = Figure(figsize=(10, 9), facecolor='#f0f0f0')
        
                                                         
        ax1 = fig.add_subplot(2, 2, (1, 2))
        grade_counts = stats.get('students_by_grade', {})
        if grade_counts:
            grades = list(grade_counts.keys())
            counts = list(grade_counts.values())
            colors = ['#27ae60', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
            wedges, texts, autotexts = ax1.pie(counts, labels=grades, autopct='%1.1f%%', 
                                                startangle=90, colors=colors, textprops={'fontsize': 13})
                                                  
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(12)
                autotext.set_fontweight('bold')
                                
            for text in texts:
                text.set_fontsize(14)
                text.set_fontweight('bold')
            ax1.set_title('Grade Distribution', fontsize=14, fontweight='bold', pad=15)
        
                                         
        ax2 = fig.add_subplot(2, 2, 3)
        subject_avgs = stats.get('subject_averages', {})
        if subject_avgs:
            subjects = list(subject_avgs.keys())
            averages = list(subject_avgs.values())
            bars = ax2.barh(subjects, averages, color='#3498db')
            ax2.set_xlabel('Average (%)', fontsize=11)
            ax2.set_title('Subject Averages', fontsize=13, fontweight='bold', pad=10)
            ax2.set_xlim(0, 100)
            ax2.tick_params(axis='both', labelsize=10)
            
                                      
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax2.text(width + 1, bar.get_y() + bar.get_height()/2, 
                        f'{averages[i]:.1f}%', va='center', fontsize=10, fontweight='bold')
        
                                                            
        ax3 = fig.add_subplot(2, 2, 4)
        top_performers = stats.get('top_performers', [])
        bottom_performers = stats.get('bottom_performers', [])
        
        if top_performers or bottom_performers:
            performers = []
            scores = []
            colors_perf = []
            
                                
            for name, avg in top_performers[:5]:
                performers.append(f"{name} (Top)")
                scores.append(avg)
                colors_perf.append('#27ae60')
            
                                   
            for name, avg in bottom_performers[:5]:
                performers.append(f"{name} (Low)")
                scores.append(avg)
                colors_perf.append('#e74c3c')
            
            if performers:
                y_pos = range(len(performers))
                bars = ax3.barh(y_pos, scores, color=colors_perf)
                ax3.set_yticks(y_pos)
                ax3.set_yticklabels(performers, fontsize=9)
                ax3.set_xlabel('Average (%)', fontsize=11)
                ax3.set_title('Top & Bottom Performers', fontsize=13, fontweight='bold', pad=10)
                ax3.set_xlim(0, 100)
                ax3.tick_params(axis='y', labelsize=9)
                
                                  
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax3.text(width + 1, bar.get_y() + bar.get_height()/2, 
                            f'{scores[i]:.1f}%', va='center', fontsize=9, fontweight='bold')
        
        fig.tight_layout(pad=2.5)
        
                                     
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
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
