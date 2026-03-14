import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
import calendar
import random
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

MOTIVATIONAL_QUOTES = [
    "The only way to learn a new programming language is by writing programs in it. — Dennis Ritchie",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Code is like humor. When you have to explain it, it’s bad. — Cory House",
    "The best way to predict the future is to create it. — Peter Drucker",
    "Believe you can and you’re halfway there. — Theodore Roosevelt",
    "It always seems impossible until it’s done. — Nelson Mandela",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
    "The only way to do great work is to love what you do. — Steve Jobs",
    "Your time is limited, so don’t waste it living someone else’s life. — Steve Jobs",
    "Innovation distinguishes between a leader and a follower. — Steve Jobs",
    "The question of whether machines can think is about as relevant as the question of whether submarines can swim. — Edsger W. Dijkstra",
    "AI is the new electricity. — Andrew Ng",
    "Data is the new oil. — Clive Humby",
    "Programming is the closest thing we have to magic. — Drew Houston",
    "Every great developer got there by solving problems they were unqualified to solve. — Patrick McKenzie",
    "Intelligence is the ability to adapt to change. — Stephen Hawking",
    "Education is not the learning of facts, but the training of the mind to think. — Albert Einstein",
    "The future belongs to the curious. — Anonymous",
    "Stay hungry, stay foolish. — Steve Jobs",
    "The mind is everything. What you think you become. — Buddha",
    "Don’t stop until you’re proud.",
    "Small steps every day lead to big results.",
    "Consistency is the key to mastery.",
    "Hardships often prepare ordinary people for an extraordinary destiny. — C.S. Lewis",
    "The people who are crazy enough to think they can change the world are the ones who do. — Rob Siltanen"
]

PHASES = [
    {
        "name": "Phase 1: Python Mastery", 
        "desc": "Python Basics, Pandas, NumPy", 
        "target": 20,
        "roadmap": [
            ("Core Python Syntax", ["Loops (for/while)", "Conditionals (if/else)", "Functions & *args/**kwargs"]),
            ("Object Oriented Programming", ["Classes & Objects", "Inheritance & Polymorphism", "Decorators & Generators"]),
            ("NumPy (The AI Foundation)", ["Arrays & Broadcasting", "Vectorization (Avoiding Loops)", "Universal Functions (ufuncs)"]),
            ("Pandas (Data Science)", ["DataFrames & Series", "Cleaning (Handling NaNs)", "GroupBy & Pivoting", "Merging/Joining Data"]),
            ("Data Visualization", ["Matplotlib Pyplot", "Seaborn Styling", "Drawing Error Bars"])
        ]
    },
    {
        "name": "Phase 2: Essential Math", 
        "desc": "Linear Algebra, Calculus for AI", 
        "target": 20,
        "roadmap": [
            ("Linear Algebra", ["Matrix Multiplications", "Eigenvalues & Eigenvectors", "Singular Value Decomposition (SVD)"]),
            ("Calculus for AI", ["Derivatives & Chain Rule", "Partial Derivatives", "Jacobians & Hessians"]),
            ("Boolean Logic & Gates", ["OR, AND, NOT, NAND, XOR", "Mathematical Gate Formulas", "Logic Gate Composition"]),
            ("Probability & Stats", ["Distributions (Normal, Bernoulli)", "Central Limit Theorem", "Bayes Theorem"]),
            ("Optimization", ["Gradient Descent Logic", "Learning Rate Schedulers", "Momentum & Adam Optimizers"])
        ]
    },
    {
        "name": "Phase 3: Machine Learning", 
        "desc": "Scikit-Learn, Classic Algorithms", 
        "target": 30,
        "roadmap": [
            ("Supervised Learning", ["Linear & Logistic Regression", "Decision Trees & Random Forests", "SVMs & k-NN"]),
            ("Unsupervised Learning", ["k-Means Clustering", "PCA (Dimensionality Reduction)", "Anomaly Detection"]),
            ("Model Evaluation", ["Confusion Matrix", "Precision/Recall/F1", "ROC & AUC Curves", "Cross-Validation"]),
            ("Feature Engineering", ["Scaling (Standard vs MinMax)", "Encoding (One-Hot, Ordinal)", "Handling Outliers"])
        ]
    },
    {
        "name": "Phase 4: Deep Learning", 
        "desc": "PyTorch, HuggingFace, Transformers", 
        "target": 40,
        "roadmap": [
            ("Neural Networks", ["Backpropagation", "Activation Functions (ReLU, Softmax)", "Dropout & Regularization"]),
            ("Computer Vision", ["Convolution Layers (CNNs)", "Pooling & Stride", "Transfer Learning (ResNet/ViT)"]),
            ("Sequence Models", ["RNNs & LSTMs", "Word Embeddings (Word2Vec)", "Attention Mechanisms"]),
            ("Transformers", ["Encoder-Decoder Architecture", "Multi-Head Attention", "Positional Encoding", "BERT & GPT Training"])
        ]
    },
    {
        "name": "Phase 5: Portfolio Projects", 
        "desc": "RAG, API Deployment, LLM Apps", 
        "target": 50,
        "roadmap": [
            ("LLM Application Layers", ["LangChain & LlamaIndex", "Agents & Tools", "Prompt Engineering Techniques"]),
            ("RAG Systems", ["Document Loaders", "Vector Embedding Models", "Retrieval Strategies (Top-K)"]),
            ("Deployment", ["FastAPI Backend", "Dockerizing Apps", "Streamlit/Vercel Frontend", "Monitoring & Logging"]),
            ("Vector Databases", ["Indexing (HNSW/IVF)", "Metadata Filtering", "Semantic Search"])
        ]
    },
]

class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Tracker")
        self.data = self.load_data()
        
        # Load saved or default geometry
        saved_settings = self.data.get("settings", {})
        self.width = saved_settings.get("width", 1000)
        self.height = saved_settings.get("height", 760)
        
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Overlay with Taskbar support
        self.root.overrideredirect(True) # Frameless
        
        # Windows Hack for Taskbar visibility
        self.root.after(10, lambda: self.set_appwindow())
        
        # Windows Hack for Re-mapping frameless window after minimize
        self.root.bind("<Map>", self.on_map)
        
        # State
        # (self.data already loaded above for geometry)
        self.active_theme = self.data.get("settings", {}).get("theme", "Steam")
        self.colors = THEMES.get(self.active_theme, THEMES["Steam"])
        
        self.active_phase = None
        self.start_time = None
        self.is_tracking = False
        self.current_view = "dashboard"
        self.active_roadmap = None
        self.graph_range = "7D" # 7D, Month, Year, Total
        self.reset_confirm_level = 0
        self.is_fullscreen = False
        self.prev_geometry = f"{self.width}x{self.height}"
        self.search_query = tk.StringVar()
        self.search_query.trace_add("write", lambda *args: self.render_knowledge_overview())
        
        # Resizing state
        self.resizing = False
        
        # Calendar State
        now = datetime.now()
        self.cal_year = now.year
        self.cal_month = now.month
        
        # Dragging & Resizing logic
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        
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

    def minimize_window(self):
        # To minimize a frameless window: turn off frameless, stay in taskbar, then iconify
        self.root.overrideredirect(False)
        self.root.update_idletasks()
        self.root.iconify()

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.prev_geometry = self.root.geometry()
            # Get screen size
            w = self.root.winfo_screenwidth()
            h = self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}+0+0")
            self.is_fullscreen = True
        else:
            self.root.geometry(self.prev_geometry)
            self.is_fullscreen = False
        
        self.setup_ui()

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "daily_logs": {datetime.now().strftime("%Y-%m-%d"): {phase["name"]: 0.0 for phase in PHASES}},
            "knowledge_log": {phase["name"]: [] for phase in PHASES},
            "settings": {"theme": "Steam", "width": 1000, "height": 760}
        }

    def save_data(self):
        self.data["settings"]["theme"] = self.active_theme
        self.data["settings"]["width"] = self.width
        self.data["settings"]["height"] = self.height
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
        
        nav_items = [("DASH", "NAV", "dashboard"), ("CAL", "CAL", "calendar"), ("LEARN", "KNOWLEDGE", "knowledge_overview"), ("STAT", "STATS", "graphs"), ("SET", "SETTINGS", "settings")]
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
        close_btn = tk.Label(title_bar, text="X", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI Symbol", 10, "bold"), padx=10, cursor="hand2")
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())

        hide_btn = tk.Label(title_bar, text="-", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI Symbol", 10, "bold"), padx=10, cursor="hand2")
        hide_btn.pack(side="right")
        hide_btn.bind("<Button-1>", lambda e: self.minimize_window())

        full_btn = tk.Label(title_bar, text="FS", fg=self.colors["text"], bg=self.colors["bg"], font=("Segoe UI Symbol", 10, "bold"), padx=10, cursor="hand2")
        full_btn.pack(side="right")
        full_btn.bind("<Button-1>", lambda e: self.toggle_fullscreen())

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
        elif self.current_view == "roadmap":
            self.render_roadmap()
        elif self.current_view == "knowledge_overview":
            self.render_knowledge_overview()

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

        # Motivational Quote
        quote_frame = tk.Frame(self.content_frame, bg=self.colors["card"], padx=15, pady=10)
        quote_frame.pack(fill="x", pady=(0, 20))
        
        random_quote = random.choice(MOTIVATIONAL_QUOTES)
        tk.Label(quote_frame, text=f"“{random_quote}”", fg=self.colors["text"], bg=self.colors["card"], 
                 font=("Verdana", 8, "italic"), wraplength=self.root.winfo_width()-80 if not self.is_fullscreen else 1000).pack()

        # Responsive Layout for phases
        cards_per_row = 3 if self.is_fullscreen else 1
        card_container = tk.Frame(self.content_frame, bg=self.colors["bg"])
        card_container.pack(fill="both", expand=True)

        for i, phase in enumerate(PHASES):
            card = tk.Frame(card_container, bg=self.colors["card"], padx=12, pady=10)
            if self.is_fullscreen:
                card.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
                card_container.grid_columnconfigure(i % 3, weight=1)
            else:
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

            roadmap_btn = tk.Button(ctrl_row, text="ROADMAP >", command=lambda p=phase: self.open_roadmap(p),
                                    bg=self.colors["card"], fg=self.colors["accent"], relief="flat", font=("Verdana", 7, "bold"))
            roadmap_btn.pack(side="right", padx=5)

            # Map phase name to notebook filename
            nb_filename = phase["name"].replace(": ", "_").replace(" ", "_") + ".ipynb"
            nb_btn = tk.Button(ctrl_row, text="MASTER NOTEBOOK", command=lambda f=nb_filename: self.open_notebook(f),
                                 bg=self.colors["card"], fg=self.colors["positive"], relief="flat", font=("Verdana", 7, "bold"))
            nb_btn.pack(side="right", padx=5)

            if self.is_tracking and self.active_phase == phase["name"]:
                status.config(text="ACTIVE")
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

    def open_roadmap(self, phase):
        self.active_roadmap = phase
        self.switch_view("roadmap")

    def render_roadmap(self):
        phase = self.active_roadmap
        if not phase: return self.switch_view("dashboard")

        # Scrollable content for deep curriculum
        canvas = tk.Canvas(self.content_frame, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors["bg"])

        # Update scrollregion
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Create window inside canvas
        window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        # Sync width
        def sync_width(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", sync_width)
        
        # Mousewheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Header
        back_btn = tk.Button(scroll_frame, text="< BACK TO DASHBOARD", command=lambda: self.switch_view("dashboard"),
                             bg=self.colors["bg"], fg=self.colors["accent"], relief="flat", font=("Verdana", 8, "bold"))
        back_btn.pack(anchor="w", pady=(0, 10))

        tk.Label(scroll_frame, text=phase["name"].upper(), fg=self.colors["highlight"], bg=self.colors["bg"], font=("Verdana", 14, "bold")).pack(anchor="w")
        tk.Label(scroll_frame, text=phase["desc"], fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 10, "italic")).pack(anchor="w", pady=(0, 20))

        tk.Label(scroll_frame, text="DEEP-DIVE ROADMAP", fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 10, "bold")).pack(anchor="w", pady=(0, 15))

        # Roadmap Grid
        for i, (topic, subtopics) in enumerate(phase["roadmap"]):
            topic_card = tk.Frame(scroll_frame, bg=self.colors["card"], padx=15, pady=15)
            topic_card.pack(fill="x", pady=10)
            
            # Topic Header
            header = tk.Frame(topic_card, bg=self.colors["card"])
            header.pack(fill="x")
            
            tk.Label(header, text=f"{i+1}", fg=self.colors["bg"], bg=self.colors["accent"], width=3, font=("Verdana", 9, "bold")).pack(side="left", padx=(0, 10))
            tk.Label(header, text=topic.upper(), fg=self.colors["highlight"], bg=self.colors["card"], font=("Verdana", 10, "bold")).pack(side="left")
            
            # Subtopics (Deep Dive)
            sub_frame = tk.Frame(topic_card, bg=self.colors["card"], padx=40)
            sub_frame.pack(fill="x", pady=(10, 0))
            
            for sub in subtopics:
                row = tk.Frame(sub_frame, bg=self.colors["card"])
                row.pack(fill="x", pady=3)
                tk.Label(row, text="•", fg=self.colors["accent"], bg=self.colors["card"]).pack(side="left")
                tk.Label(row, text=sub, fg=self.colors["text"], bg=self.colors["card"], font=("Verdana", 9)).pack(side="left", padx=10)

        # Knowledge Log Section
        log_section = tk.Frame(scroll_frame, bg=self.colors["bg"], pady=30)
        log_section.pack(fill="x")
        
        tk.Label(log_section, text="LEARNING JOURNAL", fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 10, "bold")).pack(anchor="w")
        
        input_frame = tk.Frame(log_section, bg=self.colors["card"], padx=15, pady=15)
        input_frame.pack(fill="x", pady=10)
        
        tk.Label(input_frame, text="What did you master today?", fg=self.colors["text"], bg=self.colors["card"], font=("Verdana", 8)).pack(anchor="w")
        
        self.note_entry = tk.Entry(input_frame, bg=self.colors["bg"], fg=self.colors["highlight"], insertbackground=self.colors["accent"], relief="flat", font=("Verdana", 10))
        self.note_entry.pack(fill="x", pady=10)
        self.note_entry.bind("<Return>", lambda e: self.save_knowledge_note())
        
        tk.Button(input_frame, text="LOG KNOWLEDGE", command=self.save_knowledge_note, bg=self.colors["accent"], fg=self.colors["bg"], relief="flat", font=("Verdana", 8, "bold")).pack(side="right")

        # History
        history_frame = tk.Frame(log_section, bg=self.colors["bg"])
        history_frame.pack(fill="x", pady=20)
        
        log_data = self.data.get("knowledge_log", {}).get(phase["name"], [])
        if log_data:
            for log_entry in reversed(log_data):
                entry_f = tk.Frame(history_frame, bg=self.colors["card"], padx=10, pady=8)
                entry_f.pack(fill="x", pady=4)
                
                tk.Label(entry_f, text=log_entry["date"], fg=self.colors["accent"], bg=self.colors["card"], font=("Verdana", 7, "bold")).pack(anchor="w")
                tk.Label(entry_f, text=log_entry["note"], fg=self.colors["text"], bg=self.colors["card"], font=("Verdana", 9), wraplength=300 if not self.is_fullscreen else 1000, justify="left").pack(anchor="w")
        else:
            tk.Label(history_frame, text="No entries yet. Start logging your wins!", fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 8, "italic")).pack(pady=10)

    def render_knowledge_overview(self):
        # Header & Search
        header_f = tk.Frame(self.content_frame, bg=self.colors["bg"])
        header_f.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_f, text="KNOWLEDGE REPOSITORY", fg=self.colors["accent"], bg=self.colors["bg"], font=("Verdana", 14, "bold")).pack(side="left")
        
        search_f = tk.Frame(self.content_frame, bg=self.colors["card"], padx=10, pady=5)
        search_f.pack(fill="x", pady=(0, 15))
        
        tk.Label(search_f, text="SEARCH", fg=self.colors["text"], bg=self.colors["card"]).pack(side="left")
        search_entry = tk.Entry(search_f, textvariable=self.search_query, bg=self.colors["card"], fg=self.colors["highlight"], 
                                insertbackground=self.colors["accent"], relief="flat", font=("Verdana", 9))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        if not self.search_query.get():
            search_entry.insert(0, "Search by keyword or code...")
            search_entry.config(fg=self.colors["text"])
            search_entry.bind("<FocusIn>", lambda e: (search_entry.delete(0, tk.END), search_entry.config(fg=self.colors["highlight"])) if self.search_query.get() == "" else None)

        # Scrollable area
        canvas = tk.Canvas(self.content_frame, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        def sync_width(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", sync_width)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Collect all logs and sort by date
        all_logs = []
        query = self.search_query.get().lower()

        for phase_name, logs in self.data.get("knowledge_log", {}).items():
            for log in logs:
                if not query or query in log["note"].lower() or query in phase_name.lower():
                    all_logs.append({**log, "phase": phase_name})
        
        # Sort by date (YYYY-MM-DD HH:MM) descending
        all_logs.sort(key=lambda x: x["date"], reverse=True)

        if not all_logs:
            tk.Label(scroll_frame, text="No knowledge logged yet. Keep studying!", fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 9, "italic")).pack(pady=50)
            return

        for log in all_logs:
            card = tk.Frame(scroll_frame, bg=self.colors["card"], padx=15, pady=15)
            card.pack(fill="x", pady=5)
            
            top_row = tk.Frame(card, bg=self.colors["card"])
            top_row.pack(fill="x")
            
            tk.Label(top_row, text=log["phase"].upper(), fg=self.colors["accent"], bg=self.colors["card"], font=("Verdana", 7, "bold")).pack(side="left")
            tk.Label(top_row, text=log["date"], fg=self.colors["text"], bg=self.colors["card"], font=("Verdana", 7)).pack(side="right")
            
            # Note with wraplength
            note_lbl = tk.Label(card, text=log["note"], fg=self.colors["highlight"], bg=self.colors["card"], font=("Verdana", 9), justify="left", wraplength=350 if not self.is_fullscreen else 1100)
            note_lbl.pack(anchor="w", pady=(10, 0))
            
            # Detect code/formulas and style them if possible (simple split)
            if "def " in log["note"] or "AND=" in log["note"]:
                note_lbl.config(font=("Consolas", 9) if not self.is_fullscreen else ("Consolas", 10))

    def open_notebook(self, filename):
        try:
            # Use script directory for relative file lookups
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, filename)
            
            if os.path.exists(full_path):
                os.startfile(os.path.normpath(full_path))
            else:
                messagebox.showerror("Error", f"Notebook file not found at:\n{full_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Windows could not launch the notebook.\n\nError: {e}\n\nTip: Ensure you have an app like VS Code or a browser associated with .ipynb files.")

    def save_knowledge_note(self):
        note = self.note_entry.get().strip()
        if not note: return
        
        phase_name = self.active_roadmap["name"]
        if "knowledge_log" not in self.data:
            self.data["knowledge_log"] = {}
        if phase_name not in self.data["knowledge_log"]:
            self.data["knowledge_log"][phase_name] = []
            
        self.data["knowledge_log"][phase_name].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": note
        })
        
        self.save_data()
        self.render_roadmap() # Refresh view

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
        can_w = 1100 if self.is_fullscreen else 380
        self.canvas = tk.Canvas(self.content_frame, width=can_w, height=300, bg=self.colors["bg"], highlightthickness=0)
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
        full_w = 1040 if self.is_fullscreen else 320
        x_step = full_w / (len(plot_data) - 1) if len(plot_data) > 1 else 0
        for i, (label, val) in enumerate(plot_data):
            x = 40 + (i * x_step)
            y = 260 - (val / max_val) * 220
            points.extend([x, y])
            
            # X-axis label (only show some if too many)
            label_limit = 30 if self.is_fullscreen else 15
            if len(plot_data) < label_limit or i % (len(plot_data)//(label_limit//2) + 1) == 0:
                self.canvas.create_text(x, 280, text=label, fill=self.colors["text"], font=("Verdana", 7))

        if len(points) >= 4:
            self.canvas.create_line(points, fill=self.colors["accent"], width=3 if self.is_fullscreen else 2, smooth=True)
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

        tk.Label(self.content_frame, text="WINDOW DIMENSIONS", fg=self.colors["text"], bg=self.colors["bg"], font=("Verdana", 8, "bold")).pack(pady=(20, 5))
        
        dim_frame = tk.Frame(self.content_frame, bg=self.colors["bg"])
        dim_frame.pack(pady=5)
        
        tk.Label(dim_frame, text="W:", fg=self.colors["text"], bg=self.colors["bg"]).pack(side="left")
        self.w_entry = tk.Entry(dim_frame, width=5, bg=self.colors["card"], fg=self.colors["highlight"], relief="flat")
        self.w_entry.insert(0, str(self.width))
        self.w_entry.pack(side="left", padx=5)
        
        tk.Label(dim_frame, text="H:", fg=self.colors["text"], bg=self.colors["bg"]).pack(side="left")
        self.h_entry = tk.Entry(dim_frame, width=5, bg=self.colors["card"], fg=self.colors["highlight"], relief="flat")
        self.h_entry.insert(0, str(self.height))
        self.h_entry.pack(side="left", padx=5)
        
        tk.Button(dim_frame, text="APPLY", command=self.apply_dimensions, bg=self.colors["accent"], fg=self.colors["bg"], relief="flat", font=("Verdana", 7, "bold"), padx=10).pack(side="left", padx=10)

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

    def apply_dimensions(self):
        try:
            w = int(self.w_entry.get())
            h = int(self.h_entry.get())
            if w < 400 or h < 400:
                raise ValueError("Too small")
            self.width, self.height = w, h
            self.root.geometry(f"{self.width}x{self.height}")
            self.save_data()
            self.setup_ui()
        except:
            messagebox.showerror("Error", "Invalid dimensions. Minimum: 400x400.")

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

    def on_click(self, event):
        # Determine if we are resizing (bottom right corner) or moving
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_width = self.root.winfo_width()
        self.start_height = self.root.winfo_height()
        
        # Resize grip area (bottom 20px, right 20px)
        if event.x > self.start_width - 20 and event.y > self.start_height - 20:
            self.resizing = True
        else:
            self.resizing = False
            self.x = event.x
            self.y = event.y

    def on_drag(self, event):
        if self.resizing:
            new_width = max(400, self.start_width + (event.x_root - self.start_x))
            new_height = max(400, self.start_height + (event.y_root - self.start_y))
            self.root.geometry(f"{new_width}x{new_height}")
            self.width, self.height = new_width, new_height
            # Don't save on every tick for performance, just update state
        else:
            # Move Logic
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
            
    def stop_drag(self, event):
        if self.resizing:
            self.save_data() # Save dimensions on release
        self.resizing = False

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
