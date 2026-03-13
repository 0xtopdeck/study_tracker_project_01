import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Configuration & Styling ---
SAVE_FILE = "save_game.json"
THEME_COLOR_BG = "#1b2838"  # Steam Dark Blue
THEME_COLOR_CARD = "#2a475e" # Steam Lighter Blue
THEME_COLOR_ACCENT = "#66c0f4" # Steam Sky Blue
THEME_COLOR_TEXT = "#c7d5e0"
THEME_COLOR_HIGHLIGHT = "#ffffff"

PHASES = [
    {"name": "Phase 1: Python Mastery", "desc": "Python Basics, Pandas, NumPy", "target": 20},
    {"name": "Phase 2: Essential Math", "desc": "Linear Algebra, Calculus for AI", "target": 20},
    {"name": "Phase 3: Machine Learning", "desc": "Scikit-Learn, Classic Algorithms", "target": 30},
    {"name": "Phase 4: Deep Learning", "desc": "PyTorch, HuggingFace, Transformers", "target": 40},
    {"name": "Phase 5: Portfolio Projects", "desc": "RAG, API Deployment, LLM Apps", "target": 50},
]

class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Tracker")
        self.root.geometry("450x700")
        self.root.configure(bg=THEME_COLOR_BG)
        
        # Data storage
        self.data = self.load_data()
        
        self.setup_ui()
        self.update_total_hours()

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        # Default data if no save file exists
        return {phase["name"]: 0 for phase in PHASES}

    def save_data(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.data, f)

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=THEME_COLOR_BG, pady=20)
        header_frame.pack(fill="x")

        self.total_label = tk.Label(
            header_frame, 
            text="TOTAL HOURS PLAYED: 0", 
            fg=THEME_COLOR_ACCENT, 
            bg=THEME_COLOR_BG,
            font=("Verdana", 14, "bold")
        )
        self.total_label.pack()

        subtitle = tk.Label(
            header_frame,
            text="Leveling up to Junior AI Engineer",
            fg=THEME_COLOR_TEXT,
            bg=THEME_COLOR_BG,
            font=("Verdana", 9, "italic")
        )
        subtitle.pack()

        # Phase Cards Container
        self.scroll_frame = tk.Frame(self.root, bg=THEME_COLOR_BG)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.phase_widgets = {}

        for phase in PHASES:
            card = tk.Frame(self.scroll_frame, bg=THEME_COLOR_CARD, bd=1, relief="flat", padx=15, pady=10)
            card.pack(fill="x", pady=5)

            # Title & Description
            title_label = tk.Label(
                card, 
                text=phase["name"].upper(), 
                fg=THEME_COLOR_HIGHLIGHT, 
                bg=THEME_COLOR_CARD,
                font=("Verdana", 10, "bold")
            )
            title_label.pack(anchor="w")

            desc_label = tk.Label(
                card,
                text=phase["desc"],
                fg=THEME_COLOR_TEXT,
                bg=THEME_COLOR_CARD,
                font=("Verdana", 8)
            )
            desc_label.pack(anchor="w")

            # Progress Bar Section
            progress_frame = tk.Frame(card, bg=THEME_COLOR_CARD, pady=5)
            progress_frame.pack(fill="x")

            # Style the progress bar
            style = ttk.Style()
            style.theme_use('default')
            style.configure("Steam.Horizontal.TProgressbar", 
                            troughcolor=THEME_COLOR_BG, 
                            background=THEME_COLOR_ACCENT,
                            thickness=10)

            pb = ttk.Progressbar(
                progress_frame, 
                style="Steam.Horizontal.TProgressbar",
                orient="horizontal", 
                length=200, 
                mode="determinate"
            )
            pb.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            hours_val = self.data.get(phase["name"], 0)
            pb["maximum"] = phase["target"]
            pb["value"] = hours_val

            stats_label = tk.Label(
                progress_frame,
                text=f"{hours_val}/{phase['target']} hrs",
                fg=THEME_COLOR_TEXT,
                bg=THEME_COLOR_CARD,
                font=("Verdana", 8, "bold"),
                width=10
            )
            stats_label.pack(side="right")

            # Controls
            btn_frame = tk.Frame(card, bg=THEME_COLOR_CARD)
            btn_frame.pack(fill="x", pady=(5, 0))

            add_btn = tk.Button(
                btn_frame,
                text="+1 HOUR",
                command=lambda p=phase["name"]: self.add_hour(p),
                bg=THEME_COLOR_ACCENT,
                fg=THEME_COLOR_BG,
                font=("Verdana", 8, "bold"),
                relief="flat",
                activebackground=THEME_COLOR_HIGHLIGHT,
                padx=10
            )
            add_btn.pack(side="right")

            self.phase_widgets[phase["name"]] = {
                "pb": pb,
                "label": stats_label,
                "target": phase["target"]
            }

        # Footer / Reset
        footer = tk.Frame(self.root, bg=THEME_COLOR_BG, pady=10)
        footer.pack(fill="x")
        
        save_btn = tk.Button(
            footer,
            text="FORCE SAVE GAME",
            command=self.save_data,
            bg=THEME_COLOR_BG,
            fg=THEME_COLOR_TEXT,
            font=("Verdana", 7),
            relief="flat"
        )
        save_btn.pack()

    def add_hour(self, phase_name):
        self.data[phase_name] += 1
        self.update_ui_for_phase(phase_name)
        self.update_total_hours()
        self.save_data()

    def update_ui_for_phase(self, phase_name):
        widgets = self.phase_widgets[phase_name]
        hours = self.data[phase_name]
        target = widgets["target"]
        
        widgets["pb"]["value"] = min(hours, target) # Cap visual at 100%
        widgets["label"].config(text=f"{hours}/{target} hrs")
        
        if hours >= target:
            widgets["label"].config(fg="#a4cf51") # Achievement green

    def update_total_hours(self):
        total = sum(self.data.values())
        self.total_label.config(text=f"TOTAL HOURS PLAYED: {total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()
