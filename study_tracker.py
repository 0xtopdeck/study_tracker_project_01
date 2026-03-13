import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
import calendar
from datetime import datetime, timedelta

# --- Configuration & Styling ---
SAVE_FILE = "save_game.json"

THEMES = {
    "Steam": {
        "bg": "#1b2838",
        "card": "#2a475e",
        "accent": "#66c0f4",
        "text": "#c7d5e0",
        "highlight": "#ffffff",
        "positive": "#a4cf51",
        "negative": "#d9534f"
    },
    "AMOLED": {
        "bg": "#000000",
        "card": "#1a1a1a",
        "accent": "#ffffff",
        "text": "#888888",
        "highlight": "#ffffff",
        "positive": "#00ff00",
        "negative": "#ff0000"
    },
    "Cyberpunk": {
        "bg": "#020d18",
        "card": "#05162a",
        "accent": "#00ff9f",
        "text": "#00b8ff",
        "highlight": "#d600ff",
        "positive": "#f7ff00",
        "negative": "#ff0055"
    }
}

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
        self.root.geometry("420x760")
        
        # Overlay with Taskbar support
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True) # Frameless
        
        # Windows Hack for Taskbar visibility
        self.root.after(10, lambda: self.set_appwindow())
        
        # Windows Hack for Re-mapping frameless window after minimize
        self.root.bind("<Map>", self.on_map)
        
        # State
        self.data = self.load_data()
        self.active_theme = self.data.get("settings", {}).get("theme", "Steam")
        self.colors = THEMES.get(self.active_theme, THEMES["Steam"])
        
        self.active_phase = None
        self.start_time = None
        self.is_tracking = False
        self.current_view = "dashboard"
        self.graph_range = "7D" # 7D, Month, Year, Total
        self.reset_confirm_level = 0
        
        # Calendar State
        now = datetime.now()
        self.cal_year = now.year
        self.cal_month = now.month
        
        # Dragging logic
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        
        self.apply_theme()
        self.tick()

    def set_appwindow(self):
        # This hack ensures a frameless window appears in the Taskbar and Alt-Tab list
        try:
            from ctypes import windll
            hwnd = windll.user32.GetParent(self.root.winfo_id())
            # If GetParent is 0, then the root winfo_id is the main handle
            if hwnd == 0: hwnd = self.root.winfo_id()
            
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except:
            pass

    def on_map(self, event):
        # When restoring from taskbar, ensure it's still frameless and in Alt-Tab
        self.root.overrideredirect(True)
        self.set_appwindow()
        self.root.attributes("-topmost", True)

    def minimize_window(self):
        # To minimize a frameless window: turn off frameless, stay in taskbar, then iconify
        self.root.overrideredirect(False)
        self.root.update_idletasks()
        self.root.iconify()

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "daily_logs": {datetime.now().strftime("%Y-%m-%d"): {phase["name"]: 0.0 for phase in PHASES}},
            "settings": {"theme": "Steam"}
        }

    def save_data(self):
        self.data["settings"] = {"theme": self.active_theme}
        with open(SAVE_FILE, "w") as f:
            json.dump(self.data, f)

    def get_total_by_phase(self):
        totals = {phase["name"]: 0.0 for phase in PHASES}
        for date, logs in self.data.get("daily_logs", {}).items():
            for phase, hours in logs.items():
                if phase in totals:
                    totals[phase] += hours
        return totals

    def apply_theme(self):
        self.colors = THEMES.get(self.active_theme, THEMES["Steam"])
        self.root.configure(bg=self.colors["bg"])
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        style_name = f"{self.active_theme}.Horizontal.TProgressbar"
        self.style.configure(style_name, troughcolor=self.colors["bg"], background=self.colors["accent"], thickness=8, borderwidth=0)
        self.style.layout(style_name, self.style.layout("Horizontal.TProgressbar"))
        
        self.setup_ui()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.border_frame = tk.Frame(self.root, bg=self.colors["accent"], bd=1)
        self.border_frame.pack(fill="both", expand=True)
        
        self.main_container = tk.Frame(self.border_frame, bg=self.colors["bg"])
        self.main_container.pack(fill="both", expand=True, padx=1, pady=1)

        # Title Bar
        title_bar = tk.Frame(self.main_container, bg=self.colors["bg"], height=35)
        title_bar.pack(fill="x")
        
        nav_container = tk.Frame(title_bar, bg=self.colors["bg"])
        nav_container.pack(side="left", padx=5)
        
        nav_items = [("DASH", "⊞", "dashboard"), ("CAL", "📅", "calendar"), ("STAT", "📊", "graphs"), ("SET", "⚙", "settings")]
        for text, icon, view in nav_items:
            is_active = self.current_view == view
            color = self.colors["accent"] if is_active else self.colors["text"]
            
            btn_frame = tk.Frame(nav_container, bg=self.colors["bg"])
            btn_frame.pack(side="left", padx=2)
            
            l = tk.Label(btn_frame, text=f"{icon} {text}", fg=color, bg=self.colors["bg"], 
                         font=("Segoe UI Symbol", 8, "bold"), cursor="hand2", padx=2)
            l.pack()
            l.bind("<Button-1>", lambda e, v=view: self.switch_view(v))

        # Close/Minimize Buttons
        close_btn = tk.Label(title_bar, text="✕", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI Symbol", 10, "bold"), padx=10, cursor="hand2")
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())

        hide_btn = tk.Label(title_bar, text="—", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI Symbol", 10, "bold"), padx=10, cursor="hand2")
        hide_btn.pack(side="right")
        hide_btn.bind("<Button-1>", lambda e: self.minimize_window())

        # Header Time Info
        header_info = tk.Frame(self.main_container, bg=self.colors["bg"], pady=8)
        header_info.pack(fill="x")
        
        now = datetime.now()
        date_str = now.strftime("%A, %b %d")
        week_num = now.isocalendar()[1]
        
        tk.Label(header_info, text=f"{date_str} • WEEK {week_num}", fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 8, "bold")).pack()
        
        self.content_frame = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=5)

        if self.current_view == "dashboard":
            self.render_dashboard()
        elif self.current_view == "calendar":
            self.render_calendar()
        elif self.current_view == "graphs":
            self.render_graphs()
        elif self.current_view == "settings":
            self.render_settings()

    def switch_view(self, view):
        self.current_view = view
        self.setup_ui()

    def render_dashboard(self):
        totals = self.get_total_by_phase()
        total_sum = sum(totals.values())
        
        # Leveling Logic
        level = int(total_sum // 15) + 1
        xp_in_level = total_sum % 15
        xp_percent = (xp_in_level / 15) * 100

        # Level Badge & Global XP Bar
        level_frame = tk.Frame(self.content_frame, bg=self.colors["bg"])
        level_frame.pack(fill="x", pady=(0, 10))
        
        l_badge = tk.Frame(level_frame, bg=self.colors["accent"], padx=10, pady=5)
        l_badge.pack(side="left")
        
        tk.Label(l_badge, text=f"LVL {level}", fg=self.colors["bg"], bg=self.colors["accent"], 
                 font=("Verdana", 12, "bold")).pack()
        
        xp_info = tk.Frame(level_frame, bg=self.colors["bg"])
        xp_info.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        tk.Label(xp_info, text=f"GLOBAL RANK: {xp_in_level:.1f} / 15.0 XP TO NEXT LEVEL", 
                 fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 7, "bold")).pack(anchor="w")
        
        # Global XP Progress Bar
        style_xp = f"{self.active_theme}.XP.Horizontal.TProgressbar"
        self.style.configure(style_xp, troughcolor=self.colors["card"], background=self.colors["positive"], thickness=10)
        self.style.layout(style_xp, self.style.layout("Horizontal.TProgressbar"))
        
        xp_pb = ttk.Progressbar(xp_info, style=style_xp, orient="horizontal", mode="determinate")
        xp_pb.pack(fill="x", pady=(2, 0))
        xp_pb["value"] = xp_percent

        tk.Frame(self.content_frame, bg=self.colors["card"], height=1).pack(fill="x", pady=10)

        tk.Label(self.content_frame, text=f"TOTAL PLAYTIME: {total_sum:.1f} HOURS", 
                 fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 9, "bold")).pack(pady=(0,10))

        for phase in PHASES:
            card = tk.Frame(self.content_frame, bg=self.colors["card"], padx=12, pady=10)
            card.pack(fill="x", pady=4)

            title_row = tk.Frame(card, bg=self.colors["card"])
            title_row.pack(fill="x")

            tk.Label(title_row, text=phase["name"].upper(), fg=self.colors["highlight"], bg=self.colors["card"], font=("Verdana", 8, "bold")).pack(side="left")
            status = tk.Label(title_row, text="", fg=self.colors["accent"], bg=self.colors["card"], font=("Verdana", 7, "bold"))
            status.pack(side="right")

            pb = ttk.Progressbar(card, style=f"{self.active_theme}.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
            pb.pack(fill="x", pady=5)
            pb["maximum"] = phase["target"]
            pb["value"] = totals[phase["name"]]

            ctrl_row = tk.Frame(card, bg=self.colors["card"])
            ctrl_row.pack(fill="x")

            stats = tk.Label(ctrl_row, text=f"{totals[phase['name']]:.1f}/{phase['target']}h", fg=self.colors["text"], bg=self.colors["card"], font=("Verdana", 7))
            stats.pack(side="left")

            btn_text = "STOP" if self.is_tracking and self.active_phase == phase["name"] else "START"
            btn_bg = self.colors["negative"] if btn_text == "STOP" else self.colors["bg"]
            btn = tk.Button(ctrl_row, text=btn_text, command=lambda p=phase["name"]: self.toggle_tracking(p), 
                            bg=btn_bg, fg=self.colors["highlight"], relief="flat", font=("Verdana", 7, "bold"), padx=8)
            btn.pack(side="right")

            if self.is_tracking and self.active_phase == phase["name"]:
                status.config(text="● ACTIVE")
                card.config(highlightbackground=self.colors["accent"], highlightthickness=1)

    def render_calendar(self):
        header = tk.Frame(self.content_frame, bg=self.colors["bg"])
        header.pack(fill="x", pady=5)
        
        tk.Button(header, text="<", command=self.prev_month, bg=self.colors["card"], fg=self.colors["text"], relief="flat").pack(side="left")
        tk.Label(header, text=f"{calendar.month_name[self.cal_month]} {self.cal_year}".upper(), 
                 fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 10, "bold")).pack(side="left", expand=True)
        tk.Button(header, text=">", command=self.next_month, bg=self.colors["card"], fg=self.colors["text"], relief="flat").pack(side="right")

        cal_grid = tk.Frame(self.content_frame, bg=self.colors["bg"])
        cal_grid.pack(fill="both", expand=True, pady=10)

        days = ["M", "T", "W", "T", "F", "S", "S"]
        for i, d in enumerate(days):
            tk.Label(cal_grid, text=d, fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 7, "bold")).grid(row=0, column=i, pady=5)

        month_cal = calendar.monthcalendar(self.cal_year, self.cal_month)
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        for r, week in enumerate(month_cal):
            for c, day in enumerate(week):
                if day != 0:
                    date_str = f"{self.cal_year}-{self.cal_month:02d}-{day:02d}"
                    hours = sum(self.data.get("daily_logs", {}).get(date_str, {}).values())
                    
                    is_today = (date_str == today_str)
                    bg_color = self.colors["card"]
                    text_color = self.colors["highlight"]
                    
                    if hours > 0: bg_color = "#3d6482"
                    if hours > 1: bg_color = self.colors["accent"]
                    if hours > 3: bg_color = self.colors["positive"]
                    
                    border_color = self.colors["accent"] if is_today else bg_color
                    f = tk.Frame(cal_grid, bg=border_color, padx=1, pady=1)
                    f.grid(row=r+1, column=c, padx=3, pady=3)

                    btn = tk.Button(f, text=str(day), width=4, height=2, bg=bg_color, fg=text_color, 
                                    relief="flat", font=("Verdana", 8, "bold" if is_today else "normal"), 
                                    command=lambda d=date_str: self.show_date_detail(d))
                    btn.pack()

        self.date_detail_lbl = tk.Label(self.content_frame, text="Select a date for detail", 
                                       fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 8, "italic"), pady=15)
        self.date_detail_lbl.pack()

    def prev_month(self):
        self.cal_month -= 1
        if self.cal_month == 0: self.cal_month = 12; self.cal_year -= 1
        self.setup_ui()

    def next_month(self):
        self.cal_month += 1
        if self.cal_month == 13: self.cal_month = 1; self.cal_year += 1
        self.setup_ui()

    def show_date_detail(self, date_str):
        logs = self.data["daily_logs"].get(date_str, {})
        if not logs:
            self.date_detail_lbl.config(text=f"{date_str}: No study logged")
            return
        total = sum(logs.values())
        detail = f"{date_str} ({total:.1f}h)\n" + "\n".join([f"• {p[:15]}: {h:.1f}h" for p, h in logs.items() if h > 0])
        self.date_detail_lbl.config(text=detail)

    def render_graphs(self):
        tk.Label(self.content_frame, text="PROGRESS TRENDS", fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 10, "bold")).pack(pady=5)
        
        # Range Selector Navigation
        range_frame = tk.Frame(self.content_frame, bg=self.colors["bg"])
        range_frame.pack(fill="x", pady=5)
        
        for r in ["7D", "MONTH", "YEAR", "TOTAL"]:
            btn = tk.Button(range_frame, text=r, command=lambda range_val=r: self.set_graph_range(range_val),
                            bg=self.colors["card"] if self.graph_range == r else self.colors["bg"],
                            fg=self.colors["highlight"] if self.graph_range == r else self.colors["text"],
                            relief="flat", font=("Verdana", 7, "bold"), width=8)
            btn.pack(side="left", padx=2, expand=True)

        # Canvas for Linear Chart
        self.canvas = tk.Canvas(self.content_frame, width=380, height=300, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.draw_linear_graph()

    def set_graph_range(self, range_val):
        self.graph_range = range_val
        self.setup_ui()

    def draw_linear_graph(self):
        # 1. Prepare Data based on graph_range
        now = datetime.now()
        plot_data = [] # List of (label, value)
        
        if self.graph_range == "7D":
            for i in range(6, -1, -1):
                d = (now - timedelta(days=i)).strftime("%Y-%m-%d")
                val = sum(self.data.get("daily_logs", {}).get(d, {}).values())
                plot_data.append((d.split("-")[-1], val))
        
        elif self.graph_range == "MONTH":
            _, last_day = calendar.monthrange(now.year, now.month)
            for i in range(1, last_day + 1):
                d = f"{now.year}-{now.month:02d}-{i:02d}"
                val = sum(self.data.get("daily_logs", {}).get(d, {}).values())
                plot_data.append((str(i), val))
                
        elif self.graph_range == "YEAR":
            for i in range(1, 13):
                m_total = 0
                for d, logs in self.data.get("daily_logs", {}).items():
                    dt = datetime.strptime(d, "%Y-%m-%d")
                    if dt.year == now.year and dt.month == i:
                        m_total += sum(logs.values())
                plot_data.append((calendar.month_name[i][:3], m_total))
        
        else: # TOTAL (per month since inception)
            # Find earliest date
            dates = sorted(self.data.get("daily_logs", {}).keys())
            if not dates: 
                plot_data = [("N/A", 0)]
            else:
                first_dt = datetime.strptime(dates[0], "%Y-%m-%d")
                curr_dt = first_dt
                while curr_dt <= now:
                    m_str = curr_dt.strftime("%b %y")
                    m_total = 0
                    for d, logs in self.data.get("daily_logs", {}).items():
                        dt = datetime.strptime(d, "%Y-%m-%d")
                        if dt.year == curr_dt.year and dt.month == curr_dt.month:
                            m_total += sum(logs.values())
                    plot_data.append((m_str, m_total))
                    # Move to next month
                    curr_dt = (curr_dt.replace(day=1) + timedelta(days=32)).replace(day=1)

        # 2. Draw axes and legend
        max_val = max([p[1] for p in plot_data], default=1)
        if max_val == 0: max_val = 1
        
        # Draw Y-axis Labelling (Hours)
        grid_count = 5
        for i in range(grid_count + 1):
            y_val = (i / grid_count) * max_val
            y_pos = 260 - (i / grid_count) * 220
            # Grid Line
            self.canvas.create_line(40, y_pos, 360, y_pos, fill=self.colors["card"], dash=(2, 2))
            # Label
            self.canvas.create_text(35, y_pos, text=f"{y_val:.1f}h", fill=self.colors["text"], anchor="e", font=("Verdana", 7))

        # 3. Plot Line
        points = []
        x_step = 320 / (len(plot_data) - 1) if len(plot_data) > 1 else 0
        for i, (label, val) in enumerate(plot_data):
            x = 40 + (i * x_step)
            y = 260 - (val / max_val) * 220
            points.extend([x, y])
            
            # X-axis label (only show some if too many)
            if len(plot_data) < 15 or i % (len(plot_data)//7 + 1) == 0:
                self.canvas.create_text(x, 280, text=label, fill=self.colors["text"], font=("Verdana", 7))

        if len(points) >= 4:
            self.canvas.create_line(points, fill=self.colors["accent"], width=2, smooth=True)
            # Points
            for i in range(0, len(points), 2):
                x, y = points[i], points[i+1]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.colors["highlight"], outline=self.colors["accent"])

    def render_settings(self):
        tk.Label(self.content_frame, text="SETTINGS", fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 10, "bold")).pack(pady=10)
        
        tk.Label(self.content_frame, text="SELECT THEME", fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 8, "bold")).pack(pady=5)
        for theme_name in THEMES:
            btn = tk.Button(self.content_frame, text=theme_name.upper(), command=lambda t=theme_name: self.change_theme(t),
                            bg=self.colors["card"] if self.active_theme == theme_name else self.colors["bg"],
                            fg=self.colors["highlight"], relief="flat", font=("Verdana", 8), width=20, pady=5)
            btn.pack(pady=2)

        tk.Frame(self.content_frame, bg=self.colors["text"], height=1).pack(fill="x", pady=20)
        
        reset_btn_text = "RESET ALL DATA"
        if self.reset_confirm_level == 1: reset_btn_text = "ARE YOU SURE?"
        if self.reset_confirm_level == 2: reset_btn_text = "ARE YOU REALLY SURE?"
        
        reset_btn = tk.Button(self.content_frame, text=reset_btn_text, command=self.handle_reset,
                              bg=self.colors["negative"] if self.reset_confirm_level > 0 else self.colors["card"],
                              fg="white", relief="flat", font=("Verdana", 8, "bold"), width=20, pady=10)
        reset_btn.pack(pady=10)
        
        if self.reset_confirm_level > 0:
            tk.Button(self.content_frame, text="CANCEL", command=self.cancel_reset,
                      bg=self.colors["bg"], fg=self.colors["text"], relief="flat", font=("Verdana", 7)).pack()

    def change_theme(self, theme_name):
        self.active_theme = theme_name
        self.save_data()
        self.apply_theme()

    def handle_reset(self):
        self.reset_confirm_level += 1
        if self.reset_confirm_level >= 3:
            self.data = {"daily_logs": {datetime.now().strftime("%Y-%m-%d"): {phase["name"]: 0.0 for phase in PHASES}}, "settings": {"theme": self.active_theme}}
            self.save_data()
            self.reset_confirm_level = 0
            self.switch_view("dashboard")
        else:
            self.setup_ui()

    def cancel_reset(self):
        self.reset_confirm_level = 0
        self.setup_ui()

    def start_move(self, event):
        self.x = event.x; self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x; deltay = event.y - self.y
        x = self.root.winfo_x() + deltax; y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def toggle_tracking(self, phase_name):
        if self.is_tracking and self.active_phase == phase_name:
            self.stop_tracking()
        else:
            if self.is_tracking: self.stop_tracking()
            self.start_tracking(phase_name)
        self.setup_ui()

    def start_tracking(self, phase_name):
        self.is_tracking = True; self.active_phase = phase_name; self.start_time = time.time()

    def stop_tracking(self):
        if self.active_phase: self.save_data()
        self.is_tracking = False; self.active_phase = None; self.start_time = None

    def tick(self):
        if self.is_tracking and self.active_phase:
            now = time.time()
            elapsed_seconds = now - self.start_time; self.start_time = now
            elapsed_hours = elapsed_seconds / 3600
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today not in self.data["daily_logs"]:
                self.data["daily_logs"][today] = {phase["name"]: 0.0 for phase in PHASES}
            
            self.data["daily_logs"][today][self.active_phase] += elapsed_hours
            if int(now) % 15 == 0: self.save_data()

        self.root.after(1000, self.tick)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()
