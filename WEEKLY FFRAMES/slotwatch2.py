"""
creative_watch_full.py
Single-file Tkinter GUI that shows a 24h clock and daily routine frames.
Theme: Minimalist dark with neon green / teal / emerald hues.
Shows previous, current, and next scheduled activity for the selected frame.

No external files required.
"""

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from datetime import datetime, time

# -----------------------------
# Utilities
# -----------------------------
def hm_to_minutes(hm: str) -> int:
    """Convert 'HH:MM' to minutes since midnight."""
    hh, mm = hm.split(":")
    return int(hh) * 60 + int(mm)

def in_interval(now_min: int, start_min: int, end_min: int) -> bool:
    """Check inclusive start, exclusive end (so adjacent periods don't overlap)."""
    return start_min <= now_min < end_min

def format_hm(minutes: int) -> str:
    hh = minutes // 60
    mm = minutes % 60
    return f"{hh:02d}:{mm:02d}"

# -----------------------------
# Full schedule data (13 frames)
# Each frame is a list of periods; each period is dict with start,end,activities (7 items Mon-Sun)
# -----------------------------

FRAMES = {
    "🎨 Base + Painting Frame": [
        {"start":"07:00","end":"07:30","activities":["Personal Devotion (30m)","Devotion","Devotion","Devotion","Devotion","Devotion","Rest / Reflection"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics (30m)","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Light Stretching","Reflection"]},
        {"start":"08:00","end":"08:30","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"08:30","end":"11:00","activities":["Painting Session I (2.5h)","—","Color blending & composition","Painting","Painting","Painting","Light Painting (1.5h)"]},
        {"start":"11:00","end":"12:00","activities":["Cleaning / Laundry","Cleaning","Cleaning","Cleaning","Cleaning","General Cleaning","Planning next week"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:30","activities":["Painting Session II (2.5h)","—","Lighting & texture","Painting","Painting","Painting","Baking / Relax"]},
        {"start":"15:30","end":"16:00","activities":["Break","Break","Break","Break","Break","—","—"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Help Brother","Learning Something New","Help Brother","Learning","Family Time","—"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"20:00","activities":["Reflection / Rest","Reflection","Video Ref / Inspiration","Reflection","Painting Review","Reflection","Rest"]},
    ],

    "✏️ Base + Drawing Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Light Stretch","Reflection"]},
        {"start":"08:00","end":"09:30","activities":["Drawing Session I","—","Gesture & Anatomy","Drawing","Drawing","Drawing","Light Sketching"]},
        {"start":"09:30","end":"10:30","activities":["Laundry / Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","—"]},
        {"start":"10:30","end":"12:00","activities":["Learning / Art Study","Reference Study","Perspective","Form","Shading Study","Baking","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Drawing Session II","—","Props & Armor","Drawing","Drawing","Drawing","Lore Sketch"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Help Brother","—","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Evening Drawing (1h)","—","Stylized form","Quick Studies","Quick Studies","Quick Studies","Review"]},
    ],

    "🧾 Base + Poster Design Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"12:00","activities":["Poster Design (Main Block)","—","Layout & typography","Poster","Poster","Poster","Poster (Light)"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"14:30","activities":["Learning","—","Composition theory","Canva Practice","Icon Hierarchy","Font Study","Baking"]},
        {"start":"14:30","end":"16:30","activities":["Cleaning / Laundry","Help Brother","Cleaning","Help Brother","Cleaning","Family Time","Planning"]},
        {"start":"17:00","end":"18:00","activities":["Evening Poster Edit (1h)","Adjustments","Polish","Color tweak","Finalize","Upload","Rest"]},
    ],

    "🌀 Base + Logo Design Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:30","activities":["Logo Design Block I","—","Concept sketching","Logo","Logo","Logo","Logo (Short)"]},
        {"start":"09:30","end":"11:00","activities":["Learning / Vector practice","Learning","Icon Study","Brand Form","Grid System","Baking","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Logo Design Block II","—","Vector creation","Logo","Logo","Logo","Polish"]},
        {"start":"16:00","end":"17:00","activities":["Cleaning / Help Brother","Cleaning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Upload","Reflection","Upload","Inspiration","Archive","Rest","Rest"]},
    ],

    "📜 Base + Lore Writing Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"10:00","activities":["Writing Session I","—","Story structure","Writing","Writing","Writing","Light Writing"]},
        {"start":"10:00","end":"11:00","activities":["Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","—"]},
        {"start":"11:00","end":"12:00","activities":["Learning: Narrative theory","Myth Study","Character Arcs","Tone Work","Scene Flow","Baking","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Writing Session II","—","Character development","Writing","Writing","Writing","Polish"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Help Brother","Learning","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Review","Reflection","Reading","Reflection","Proofing","Rest","Rest"]},
    ],

    "🎞️ Base + Video Editing Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:30","activities":["Cooking / Cleaning","Cooking","Cooking","Cooking","Cooking","Cleaning","—"]},
        {"start":"09:30","end":"11:30","activities":["Editing Block I","—","Clip sorting / cuts","Editing","Editing","Editing","Light Edit"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Learning","—","Color grading, audio","Learning","Study","Practice","Baking"]},
        {"start":"17:00","end":"18:00","activities":["Editing Block II","—","Reels / Sound Sync","Upload","Polish","Export","Publish"]},
        {"start":"18:00","end":"19:00","activities":["Reflection","Reflection","Reflection","Reflection","Reflection","Rest","Rest"]},
    ],

    "📊 Base + Excel Automation Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:30","activities":["Excel Automation I","—","Formula & Logic","Excel","Excel","Excel","Light Excel"]},
        {"start":"09:30","end":"11:00","activities":["Learning / Macro Study","Learning","VBA Practice","Dashboards","Testing","Baking","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Excel Automation II","—","File testing","Excel","Excel","Excel","Debug"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Cleaning","Learning","Help Brother","Cleaning","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Review","Reflection","Reflection","Reflection","Review","Rest","Rest"]},
    ],

    "🧠 Base + Front-End Development Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Reflection / Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Light Stretch","Rest"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"11:00","activities":["Front-End Dev I","—","HTML/CSS structure","Coding","UI Setup","Layout Design","Component Study"]},
        {"start":"11:00","end":"12:00","activities":["Cleaning / Laundry","Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Front-End Dev II","—","React / UX polish","Practice","Data Binding","Responsive Design","Debug"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Review / Project Journal","Reflection","Reading","Reflection","Review","Rest","Rest"]},
    ],

    "🐍 Base + Database Integration Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Light Stretch","Reflection"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"13:00","activities":["DB Integration Deep Block (4h)","—","SQL + Python connectors","Coding","Testing","CRUD Building","Query Writing"]},
        {"start":"13:00","end":"14:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"14:00","end":"15:30","activities":["Learning","—","Schema design","Data flow","Learning","Reading","Practice"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Cleaning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Code Notes","Reflection","Reflection","Reflection","Reflection","Rest","Rest"]},
    ],

    "⚙️ Base + File Automation Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Light Stretch","Reflection"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"11:00","activities":["Automation Block I","—","Python scripting","Coding","Coding","Coding","Testing"]},
        {"start":"11:00","end":"12:00","activities":["Cleaning / Organizing","Cleaning","Cleaning","Cleaning","Cleaning","Cleaning","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Automation Block II","—","File management logic","File Ops","Export","Script Format","Tool Debug"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Review","Reflection","Reflection","Reflection","Review","Rest","Rest"]},
    ],

    "🎥 Base + YouTube & Facebook Channel Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"11:00","activities":["Planning / Scripting Videos","Planning","Scripting","Voice Notes","Storyboard","Planning","—"]},
        {"start":"11:00","end":"12:00","activities":["Cleaning / Setup","Cleaning","Setup","Cleaning","Setup","Cleaning","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Editing / Filming","—","Long edit session","Edit","Film","Edit","—"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:30","activities":["Upload & Analytics Review","Upload","Community","Upload","Comments","Review","Rest"]},
    ],

    "📱 Base + TikTok / Instagram Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Rest"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Reflection"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"10:30","activities":["Content Ideation / Trends","Ideas","Concepts","Trends","Hooks","Planning","—"]},
        {"start":"10:30","end":"12:00","activities":["Cleaning / Filming Setup","Cleaning","Setup","Cleaning","Setup","Cleaning","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"15:00","activities":["Filming + Editing","Reels","Film","Edit","Film","Edit","Film"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Post & Engage","—","Upload / Comments","Post","Engage","Post","Review"]},
    ],

    "💸 Base + Digital Product Sales Frame": [
        {"start":"07:00","end":"07:30","activities":["Devotion","Devotion","Devotion","Devotion","Devotion","Devotion","Reflection"]},
        {"start":"07:30","end":"08:00","activities":["Callisthenics","Callisthenics","Callisthenics","Callisthenics","Callisthenics","Stretch","Rest"]},
        {"start":"08:00","end":"09:00","activities":["Cooking (Breakfast)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"09:00","end":"10:30","activities":["Product Creation / Design","Product Design","Product Design","Product","—","—","—"]},
        {"start":"10:30","end":"11:30","activities":["Cleaning / Upload Prep","Cleaning","Prep","Cleaning","Prep","Cleaning","—"]},
        {"start":"12:00","end":"13:00","activities":["Cooking (Lunch)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"13:00","end":"14:30","activities":["Listing / Marketing","Copy Upload","SEO","Pricing","Thumbnails","Ads","—"]},
        {"start":"14:30","end":"16:00","activities":["Shop Maintenance / Analytics","Review","Updates","Review","Updates","Review","—"]},
        {"start":"16:00","end":"17:00","activities":["Help Brother","Learning","Help Brother","Learning","Help Brother","Family","Planning"]},
        {"start":"17:00","end":"17:45","activities":["Cooking (Dinner)","Cooking","Cooking","Cooking","Cooking","Cooking","—"]},
        {"start":"18:00","end":"19:00","activities":["Reflection / Sales Notes","Reflection","Reflection","Reflection","Review","Rest","Rest"]},
    ],

}

# convert periods to numeric minute ranges and sort
for frame_name, periods in FRAMES.items():
    new_periods = []
    for p in periods:
        start_min = hm_to_minutes(p["start"])
        end_min = hm_to_minutes(p["end"])
        # guard: if end <= start (overnight), treat end as next day (not expected here)
        if end_min <= start_min:
            end_min += 24*60
        new_periods.append({
            "start_min": start_min,
            "end_min": end_min,
            "start": p["start"],
            "end": p["end"],
            "activities": p["activities"]
        })
    # sort by start_min
    new_periods.sort(key=lambda x: x["start_min"])
    FRAMES[frame_name] = new_periods

# -----------------------------
# GUI
# -----------------------------
class CreativeWatch:
    def __init__(self, root):
        self.root = root

        root.title("Personal Routine Watch")
        root.geometry("1200x850")
        root.configure(bg="#050505")
        root.resizable(False, False)

        # === Background Image ===
        self.bg_image = Image.open("PURPLE3.JPG")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                                             Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style constants
        self.bg = "#050505"
        self.card = "#0b0b0b"
        self.neon = "#00FF88"   # neon green for time
        self.teal = "#2ad1bf"   # teal text
        self.emerald = "#1fab4c" # gentle emerald accent
        self.gray = "#bfc9c6"

        # Top: title and frame selector
        header = tk.Frame(root, bg=self.bg)
        header.pack(padx=14, pady=(12,6), fill="x")

        title = tk.Label(header, text="My Personal Routine Watch", bg=self.bg, fg=self.neon,
                         font=("Segoe UI", 16, "bold"))
        title.pack(side="left")
        title = tk.Label(header, text="🕒.", bg=self.bg, fg=self.neon,
                         font=("Segoe UI", 45, "bold"))
        title.pack(side="right")

        # Combobox
        self.frame_var = tk.StringVar()
        values = list(FRAMES.keys())
        self.combo = ttk.Combobox(header, textvariable=self.frame_var, values=values, state="readonly", width=36)
        self.combo.pack(side="right", padx=(6,0))
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        # default select first
        self.frame_var.set(values[0])
        self.selected_schedule = FRAMES[self.frame_var.get()]

        # big card area
        card = tk.Frame(root, bg=self.card, bd=0, relief="ridge")
        card.pack(padx=18, pady=8, fill="both", expand=True)

        # Day label
        self.day_label = tk.Label(card, text="", bg=self.card, fg=self.gray, font=("Segoe UI", 80, "italic"))
        self.day_label.pack(pady=(12,0))

        # time label (large)
        self.time_label = tk.Label(card, text="", bg=self.card, fg=self.neon, font=("Segoe UI", 48, "bold"))
        self.time_label.pack(pady=(6,6))

        # Previous activity (smaller, above current)
        self.prev_label = tk.Label(card, text="", bg=self.card, fg=self.teal, font=("Segoe UI", 12))
        self.prev_label.pack(pady=(4,2))

        # Current activity (center)
        self.current_frame = tk.Frame(card, bg="#07110e", pady=8, padx=8)
        self.current_frame.pack(padx=24, pady=6, fill="x")
        self.current_title = tk.Label(self.current_frame, text="Current", bg="#07110e", fg=self.emerald, font=("Segoe UI", 30, "bold"))
        self.current_title.pack(anchor="w")
        self.current_label = tk.Label(self.current_frame, text="", bg="#07110e", fg="#eafaf1", font=("Segoe UI", 25), wraplength=560, justify="center")
        self.current_label.pack(pady=(6,6))

        # Next activity
        self.next_label = tk.Label(card, text="", bg=self.card, fg=self.teal, font=("Segoe UI", 12))
        self.next_label.pack(pady=(2,8))

        # Footer with quick legend / buttons
        footer = tk.Frame(root, bg=self.bg)
        footer.pack(fill="x", padx=14, pady=(0,12))
        refresh_btn = tk.Button(footer, text="Refresh Now", command=self.update_display, bg="#0d2a25", fg=self.neon, relief="flat")
        refresh_btn.pack(side="left")
        full_day_btn = tk.Button(footer, text="Show Today's Schedule", command=self.show_full_schedule, bg="#0d2a25", fg=self.teal, relief="flat")
        full_day_btn.pack(side="right")

        # schedule popup reference
        self.schedule_win = None

        # start updates
        self.update_display()
        # tick every second for clock
        self.tick()

    def on_select(self, event=None):
        self.selected_schedule = FRAMES.get(self.frame_var.get(), [])
        self.update_display()

    def find_prev_curr_next(self, now_minute: int, weekday_index: int):
        """Return (prev_entry, curr_entry, next_entry) where each is a tuple (start, end, activity) or None.
           Activity chosen is schedule.activities[weekday_index].
        """
        periods = self.selected_schedule
        prev_e = None
        curr_e = None
        next_e = None

        # flatten periods so that we can inspect them in order
        for i, p in enumerate(periods):
            # for activities that may have shorter activity arrays, guard indexing
            activities = p["activities"]
            activity = activities[weekday_index] if weekday_index < len(activities) else activities[0]
            s = p["start_min"]
            e = p["end_min"]
            if in_interval(now_minute, s, e):
                curr_e = (p["start"], p["end"], activity)
                # previous is previous period if exists
                if i - 1 >= 0:
                    prev_p = periods[i-1]
                    prev_activity = prev_p["activities"][weekday_index] if weekday_index < len(prev_p["activities"]) else prev_p["activities"][0]
                    prev_e = (prev_p["start"], prev_p["end"], prev_activity)
                # next is next period if exists
                if i + 1 < len(periods):
                    next_p = periods[i+1]
                    next_activity = next_p["activities"][weekday_index] if weekday_index < len(next_p["activities"]) else next_p["activities"][0]
                    next_e = (next_p["start"], next_p["end"], next_activity)
                break
            elif now_minute < s:
                # current time is before this period; then next is this period, previous is previous
                next_e = (p["start"], p["end"], activity)
                if i - 1 >= 0:
                    prev_p = periods[i-1]
                    prev_activity = prev_p["activities"][weekday_index] if weekday_index < len(prev_p["activities"]) else prev_p["activities"][0]
                    prev_e = (prev_p["start"], prev_p["end"], prev_activity)
                else:
                    prev_e = None
                break
            else:
                # after this period, continue — prev might be updated
                prev_activity = activity
                prev_e = (p["start"], p["end"], prev_activity)
                # continue loop to find either curr or next

        # if we didn't match any and now is after all periods, prev is last, next None
        if curr_e is None and next_e is None:
            if periods:
                last = periods[-1]
                activities = last["activities"]
                activity = activities[weekday_index] if weekday_index < len(activities) else activities[0]
                if now_minute >= last["end_min"]:
                    prev_e = (last["start"], last["end"], activity)
                    next_e = None
        return prev_e, curr_e, next_e

    def update_display(self):
        now = datetime.now()
        day_name = now.strftime("%A")
        weekday_index = now.weekday()  # Mon=0
        now_min = now.hour * 60 + now.minute

        # update time and day
        self.day_label.config(text=f"📅 {day_name}")
        self.time_label.config(text=now.strftime("%H:%M:%S"))

        # compute previous/current/next
        prev_e, curr_e, next_e = self.find_prev_curr_next(now_min, weekday_index)

        if prev_e:
            pst, pet, pact = prev_e
            self.prev_label.config(text=f"⤴ Previous: {pact}  ({pst}–{pet})")
        else:
            self.prev_label.config(text="⤴ Previous: —")

        if curr_e:
            cst, cet, cact = curr_e
            self.current_label.config(text=f"{cact}\n\n({cst}–{cet})")
            self.current_frame.config(bg="#072a1f")
            self.current_title.config(bg="#072a1f")
            self.current_label.config(bg="#072a1f")
        else:
            # when no current period, show free time
            self.current_label.config(text="Free / Unscheduled Time")
            self.current_frame.config(bg="#07110e")
            self.current_title.config(bg="#07110e")
            self.current_label.config(bg="#07110e")

        if next_e:
            nst, net, nact = next_e
            self.next_label.config(text=f"⤵ Next: {nact}  ({nst}–{net})")
        else:
            self.next_label.config(text="⤵ Next: —")

    def tick(self):
        # update every second: time and possibly activities
        self.update_display()
        self.root.after(1000, self.tick)

    def show_full_schedule(self):
        # popup that lists today's periods for the selected frame
        if self.schedule_win and tk.Toplevel.winfo_exists(self.schedule_win):
            self.schedule_win.lift()
            return
        self.schedule_win = tk.Toplevel(self.root)
        self.schedule_win.title("Today's Schedule")
        self.schedule_win.geometry("520x520")
        self.schedule_win.configure(bg=self.bg)

        day_name = datetime.now().strftime("%A")
        weekday_index = datetime.now().weekday()

        header = tk.Label(self.schedule_win, text=f"{self.frame_var.get()} — {day_name}", bg=self.bg, fg=self.neon, font=("Segoe UI", 12, "bold"))
        header.pack(pady=8)

        canvas = tk.Canvas(self.schedule_win, bg=self.card, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)

        frame_inner = tk.Frame(canvas, bg=self.card)
        canvas.create_window((0,0), window=frame_inner, anchor="nw")

        # populate
        for p in self.selected_schedule:
            s = p["start"]
            e = p["end"]
            activities = p["activities"]
            act = activities[weekday_index] if weekday_index < len(activities) else activities[0]
            row = tk.Frame(frame_inner, bg=self.card, pady=6, padx=8)
            row.pack(fill="x", padx=6, pady=4)
            tlabel = tk.Label(row, text=f"{s}–{e}", bg=self.card, fg=self.gray, width=12, anchor="w", font=("Segoe UI", 10))
            tlabel.pack(side="left")
            alabel = tk.Label(row, text=act, bg=self.card, fg=self.teal, anchor="w", font=("Segoe UI", 11), wraplength=360, justify="left")
            alabel.pack(side="left", padx=(8,0))

        # scrolling
        def on_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame_inner.bind("<Configure>", on_config)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CreativeWatch(root)
    root.mainloop()
