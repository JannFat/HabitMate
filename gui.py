# habitmate_refactored.py - REFACTORED VERSION
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, timedelta
import calendar
import random
import database as db


class HabitMateApp:
    def _init_(self, root):
        self.root = root
        self.root.title("HabitMate")
        self.root.geometry("1020x720")
        self.root.resizable(True, True)
        
        # Configuration
        self.setup_colors()
        self.setup_variables()
        self.setup_styles()
        
        # Start with login screen
        self.build_login_screen()

    def setup_colors(self):
        """Define color schemes for the application"""
        self.colors = {
            "primary": "#C89047",
            "secondary": "#A35C7A",
            "background": "#FBF5E5",
            "card_bg": "white",
            "sidebar_bg": "#A35C7A",
            "logout_bg": "#C45C3D",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336",
            "text": "#212121",
            "text_light": "#555",
            "disabled": "#888",
            "highlight": "#FFF59D",
            "completed": "#C8E6C9"
        }
        
        self.category_colors = {
            "Health": "#69E136", "Study": "#2196F3", "Fitness": "#9D3D23",
            "Work": "#9C27B0", "Personal": "#FF9800", "Mindfulness": "#00BCD4", "Social": "#E91E63"
        }

    def setup_variables(self):
        """Initialize application variables"""
        self.user_id = None
        self.habits = []
        self.completed = {}
        self.editing_index = None
        self.login_logo = None
        self.sidebar_logo = None
        self.dash = None
        self.content = None
        self.mood_label = None
        self.current_mood = "Not set"

    def setup_styles(self):
        """Define font styles"""
        self.fonts = {
            "title": ("Segoe UI", 28, "bold"),
            "subtitle": ("Segoe UI", 12),
            "heading": ("Times New Roman", 24, "bold"),
            "subheading": ("Times New Roman", 16, "bold"),
            "body": ("Times New Roman", 12),
            "small": ("Times New Roman", 10),
            "button": ("Times New Roman", 11, "bold"),
            "card_title": ("Times New Roman", 13, "bold")
        }

    # ==================== AUTHENTICATION SCREENS ====================
    
    def build_login_screen(self):
        """Build the login screen"""
        self.clear_window()
        self.root.configure(bg=self.colors["background"])
        
        # Create shadow effect container
        shadow, card = self.create_card_container(430, 530, 420, 520)
        
        # Logo
        self.create_login_logo(card)
        
        # Title
        self.create_title(card, "HABITMATE", "Calendar Habit Tracker")
        
        # Form container
        form_container = tk.Frame(card, bg=self.colors["card_bg"])
        form_container.pack(fill="both", expand=True, padx=50)
        
        # Username field
        self.login_username = self.create_form_field(
            form_container, "Username", 0, 20, is_password=False
        )
        self.login_username.focus()
        
        # Password field with eye button
        password_frame = tk.Frame(form_container, bg=self.colors["card_bg"])
        password_frame.pack(fill="x", pady=(0, 35))
        
        tk.Label(password_frame, text="Password", font=("Segoe UI", 11), 
                fg=self.colors["text_light"], bg=self.colors["card_bg"]).pack(anchor="w")
        
        pwd_entry_frame = tk.Frame(password_frame, bg=self.colors["card_bg"])
        pwd_entry_frame.pack(fill="x", pady=(8, 0))
        
        self.login_password = tk.Entry(pwd_entry_frame, width=30, font=("Segoe UI", 11), 
                                    show="●", bd=0, relief="flat",
                                    highlightthickness=2, 
                                    highlightbackground="#ddd", 
                                    highlightcolor=self.colors["primary"])
        self.login_password.pack(side="left", fill="x", expand=True, ipady=8)
        
        self.login_eye_btn = tk.Button(pwd_entry_frame, text="👁", font=("Segoe UI", 12), 
                        bg=self.colors["card_bg"], fg="#666", bd=0, cursor="hand2",
                        activebackground="#f0f0f0", 
                        command=self.toggle_login_password)
        self.login_eye_btn.pack(side="right", padx=(10, 0))
        
        # Login Button
        button_frame = tk.Frame(form_container, bg=self.colors["card_bg"])
        button_frame.pack(pady=(0, 20))
        
        tk.Button(button_frame, text="Login", bg=self.colors["primary"], fg="white", 
                font=("Segoe UI", 12, "bold"), width=16, height=1,
                bd=0, cursor="hand2", command=self.login).pack()
        
        # Register link
        self.create_auth_link(form_container, 
                            "Don't have an account?", 
                            "Create one", 
                            self.show_register_screen)

    def show_register_screen(self):
        """Build the registration screen"""
        self.clear_window()
        self.root.configure(bg=self.colors["background"])
        
        # Create shadow effect container
        shadow, card = self.create_card_container(440, 600, 430, 590)
        
        # Title (no logo on register screen)
        title_frame = tk.Frame(card, bg=self.colors["card_bg"])
        title_frame.pack(pady=(50, 40))
        
        tk.Label(title_frame, text="CREATE ACCOUNT", font=self.fonts["title"], 
                fg=self.colors["text"], bg=self.colors["card_bg"]).pack()
        tk.Label(title_frame, text="Join HabitMate to track your habits", 
                font=self.fonts["subtitle"], fg=self.colors["primary"], 
                bg=self.colors["card_bg"]).pack(pady=(5, 0))
        
        # Form container
        form_container = tk.Frame(card, bg=self.colors["card_bg"])
        form_container.pack(fill="both", expand=True, padx=60)
        
        # Username field
        self.register_username = self.create_form_field(
            form_container, "Username", 0, 20, is_password=False
        )
        self.register_username.focus()
        
        # Password field
        self.register_password, eye1 = self.create_password_field(
            form_container, "Password", 0, 20
        )
        
        # Confirm Password field
        self.register_confirm_password, eye2 = self.create_password_field(
            form_container, "Confirm Password", 0, 35
        )
        
        # Register Button
        button_frame = tk.Frame(form_container, bg=self.colors["card_bg"])
        button_frame.pack(pady=(0, 20))
        
        tk.Button(button_frame, text="Register", bg=self.colors["primary"], fg="white", 
                font=("Segoe UI", 12, "bold"), width=20, height=2,
                bd=0, cursor="hand2", command=self.register).pack()
        
        # Login link
        self.create_auth_link(form_container, 
                            "Already have an account?", 
                            "Login here", 
                            self.build_login_screen)

    # ==================== HELPER METHODS ====================

    def clear_window(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_card_container(self, shadow_w, shadow_h, card_w, card_h):
        """Create a card with shadow effect"""
        container = tk.Frame(self.root, bg=self.colors["background"])
        container.pack(fill="both", expand=True)
        
        shadow = tk.Frame(container, bg="#dddddd", width=shadow_w, height=shadow_h)
        shadow.place(relx=0.5, rely=0.5, anchor="center")
        shadow.pack_propagate(False)
        
        card = tk.Frame(container, bg=self.colors["card_bg"], width=card_w, height=card_h)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        return shadow, card

    def create_login_logo(self, parent):
        """Create logo for login screen"""
        try:
            self.login_logo = tk.PhotoImage(file="HM_logo.png").subsample(6, 6)
            logo_frame = tk.Frame(parent, bg=self.colors["card_bg"], height=60)
            logo_frame.pack(pady=(15, 5), fill="x")
            
            logo_label = tk.Label(logo_frame, image=self.login_logo, 
                                bg=self.colors["card_bg"])
            logo_label.pack()
        except Exception:
            # Fallback if logo not found
            logo_frame = tk.Frame(parent, bg=self.colors["card_bg"], height=50)
            logo_frame.pack(pady=(15, 5), fill="x")
            tk.Label(logo_frame, text="⚪ HM", font=("Times New Roman", 24, "bold"), 
                    fg=self.colors["primary"], bg=self.colors["card_bg"]).pack()

    def create_title(self, parent, title, subtitle):
        """Create title and subtitle"""
        title_frame = tk.Frame(parent, bg=self.colors["card_bg"])
        title_frame.pack(pady=(5, 25))
        
        tk.Label(title_frame, text=title, font=self.fonts["title"], 
                fg=self.colors["text"], bg=self.colors["card_bg"]).pack()
        tk.Label(title_frame, text=subtitle, font=self.fonts["subtitle"], 
                fg=self.colors["primary"], bg=self.colors["card_bg"]).pack(pady=(3, 0))

    def create_form_field(self, parent, label, top_pad, bottom_pad, is_password=False):
        """Create a form field with label and entry"""
        frame = tk.Frame(parent, bg=self.colors["card_bg"])
        frame.pack(fill="x", pady=(top_pad, bottom_pad))
        
        tk.Label(frame, text=label, font=("Segoe UI", 11), 
                fg=self.colors["text_light"], bg=self.colors["card_bg"]).pack(anchor="w")
        
        entry = tk.Entry(frame, width=30, font=("Segoe UI", 11), 
                        bd=0, relief="flat", highlightthickness=2,
                        highlightbackground="#ddd", 
                        highlightcolor=self.colors["primary"])
        
        if is_password:
            entry.config(show="●")
        
        entry.pack(fill="x", pady=(8, 0), ipady=8)
        return entry

    def create_password_field(self, parent, label, top_pad, bottom_pad):
        """Create a password field with eye toggle"""
        frame = tk.Frame(parent, bg=self.colors["card_bg"])
        frame.pack(fill="x", pady=(top_pad, bottom_pad))
        
        tk.Label(frame, text=label, font=("Segoe UI", 11), 
                fg=self.colors["text_light"], bg=self.colors["card_bg"]).pack(anchor="w")
        
        entry_frame = tk.Frame(frame, bg=self.colors["card_bg"])
        entry_frame.pack(fill="x", pady=(8, 0))
        
        entry = tk.Entry(entry_frame, width=30, font=("Segoe UI", 11), 
                        show="●", bd=0, relief="flat",
                        highlightthickness=2, highlightbackground="#ddd", 
                        highlightcolor=self.colors["primary"])
        entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        eye_btn = tk.Button(entry_frame, text="👁", font=("Segoe UI", 12), 
                        bg=self.colors["card_bg"], fg="#666", bd=0, cursor="hand2",
                        activebackground="#f0f0f0",
                        command=lambda: self.toggle_password_visibility(entry, eye_btn))
        eye_btn.pack(side="right", padx=(10, 0))
        
        return entry, eye_btn

    def create_auth_link(self, parent, text, link_text, command):
        """Create authentication link (login/register)"""
        link_frame = tk.Frame(parent, bg=self.colors["card_bg"])
        link_frame.pack()
        
        tk.Label(link_frame, text=text, fg=self.colors["text_light"], 
                bg=self.colors["card_bg"], font=("Segoe UI", 10)).pack(side="left")
        
        link = tk.Label(link_frame, text=link_text, fg=self.colors["primary"], 
                        bg=self.colors["card_bg"], font=("Segoe UI", 10, "underline"),
                        cursor="hand2")
        link.pack(side="left", padx=5)
        link.bind("<Button-1>", lambda e: command())

    def toggle_login_password(self):
        """Toggle visibility of login password"""
        if self.login_password.cget("show") == "●":
            self.login_password.config(show="")
            self.login_eye_btn.config(text="🔒")
        else:
            self.login_password.config(show="●")
            self.login_eye_btn.config(text="👁")

    def toggle_password_visibility(self, entry, button):
        """Toggle visibility of any password field"""
        if entry.cget("show") == "●":
            entry.config(show="")
            button.config(text="🔒")
        else:
            entry.config(show="●")
            button.config(text="👁")

    # ==================== AUTHENTICATION LOGIC ====================

    def login(self):
        """Handle user login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        success, user_id = db.login_user(username, password)
        if success:
            self.user_id = user_id
            self.load_user_data()
            self.root.withdraw()
            self.open_dashboard()
        else:
            messagebox.showinfo("Login Failed", "Invalid credentials!")

    def register(self):
        """Handle user registration"""
        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        success, message = db.register_user(username, password)
        if success:
            messagebox.showinfo("Registration Successful", message)
            self.build_login_screen()
        else:
            messagebox.showerror("Registration Failed", message)

    def load_user_data(self):
        """Load user habits and completion data from database"""
        self.habits = []
        self.completed = {}

        try:
            # Load habits
            rows = db.get_habits(self.user_id)
            for row in rows:
                habit_id = row[0]
                title = row[1]
                description = row[2] or ""
                
                # Parse frequency from description
                frequency = ""
                clean_description = description
                if description and "Frequency:" in description:
                    parts = description.split("Frequency:")
                    if len(parts) > 1:
                        clean_description = parts[0].strip().rstrip("|").strip()
                        frequency_part = parts[1].strip()
                        frequency = frequency_part
                
                # Parse repeat days from frequency
                repeat_days = []
                if frequency:
                    try:
                        repeat_days = [int(x) for x in str(frequency).split(",") if x.strip().isdigit()]
                    except Exception:
                        repeat_days = []

                habit_dict = {
                    "id": habit_id,
                    "name": title,
                    "category": "Personal",
                    "description": clean_description,
                    "repeat_days": repeat_days
                }
                self.habits.append(habit_dict)

            # Load completion logs
            log_rows = db.get_habit_logs(self.user_id)
            habit_id_to_index = {h["id"]: idx for idx, h in enumerate(self.habits)}
            
            for habit_id, log_date in log_rows:
                if isinstance(log_date, date):
                    day_str = log_date.isoformat()
                else:
                    day_str = str(log_date)
                
                habit_index = habit_id_to_index.get(habit_id)
                if habit_index is not None:
                    if day_str not in self.completed:
                        self.completed[day_str] = []
                    if habit_index not in self.completed[day_str]:
                        self.completed[day_str].append(habit_index)
                        
        except Exception as e:
            print(f"Error loading user data: {e}")

    # ==================== DASHBOARD ====================

    def open_dashboard(self):
        """Open the main dashboard window"""
        self.dash = tk.Toplevel(self.root)
        self.dash.title("HabitMate")
        self.dash.geometry("1020x720")
        self.dash.configure(bg=self.colors["background"])

        # Create sidebar
        self.create_sidebar()

        # Create content area
        self.content = tk.Frame(self.dash, bg=self.colors["background"])
        self.content.pack(side="right", fill="both", expand=True)

        # Mood label
        self.mood_label = tk.Label(self.content, text="Today's Mood: Not set", 
                                  font=self.fonts["body"], fg=self.colors["text"], 
                                  bg=self.colors["background"])
        self.mood_label.pack(anchor="ne", padx=20, pady=10)

        # Show home screen by default
        self.show_home()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = tk.Frame(self.dash, bg=self.colors["sidebar_bg"], width=220)
        sidebar.pack(side="left", fill="y")

        # Logo
        self.create_sidebar_logo(sidebar)

        # App name
        tk.Label(sidebar, text="HabitMate", bg=self.colors["sidebar_bg"], fg="white",
                 font=("Times New Roman", 16, "bold")).pack(pady=(0, 20))

        # Navigation buttons
        nav_items = [
            ("Home", self.show_home),
            ("Calendar", self.show_calendar),
            ("Add Habit", self.show_add_habit),
            ("View Habits", self.show_view_habits),
            ("Mood", self.open_mood_picker),
            ("Logout", self.logout)
        ]
        
        for text, command in nav_items:
            bg_color = self.colors["logout_bg"] if text == "Logout" else self.colors["primary"]
            btn = tk.Button(sidebar, text=text, width=20, height=2, bg=bg_color, 
                          fg="white", font=self.fonts["button"], command=command)
            btn.pack(pady=8, padx=10)

    def create_sidebar_logo(self, parent):
        """Create logo for sidebar"""
        try:
            self.sidebar_logo = tk.PhotoImage(file="HM_logo.png").subsample(4, 4)
            logo_sidebar = tk.Label(parent, image=self.sidebar_logo, 
                                  bg=self.colors["sidebar_bg"])
            logo_sidebar.image = self.sidebar_logo
            logo_sidebar.pack(pady=(20, 5))
        except Exception:
            logo_frame = tk.Frame(parent, bg=self.colors["sidebar_bg"], height=50)
            logo_frame.pack(pady=(20, 5), fill="x")
            tk.Label(logo_frame, text="⚪ HM", font=("Times New Roman", 20, "bold"), 
                    fg="white", bg=self.colors["sidebar_bg"]).pack()

    def clear_content(self):
        """Clear the content area"""
        for widget in self.content.winfo_children():
            if widget != self.mood_label:
                widget.destroy()

    # ==================== MAIN SCREENS ====================

    def show_home(self):
        """Display the home/dashboard screen"""
        self.clear_content()
        
        # Title
        tk.Label(self.content, text="Welcome Back!", font=self.fonts["heading"], 
                fg=self.colors["text"], bg=self.colors["background"]).pack(pady=30)

        # Random quote
        quotes = [
            "Small steps every day",
            "Consistency compounds", 
            "You're building something great",
            "Keep going!"
        ]
        tk.Label(self.content, text=random.choice(quotes), 
                font=("Times New Roman", 14, "italic"), 
                fg=self.colors["primary"], bg=self.colors["background"]).pack(pady=10)

        # Stats cards
        card_frame = tk.Frame(self.content, bg=self.colors["background"])
        card_frame.pack(pady=20)

        # Calculate stats
        today_str = date.today().isoformat()
        done_today = len(self.completed.get(today_str, []))
        total_today = sum(1 for h in self.habits if date.today().weekday() in h.get("repeat_days", []))
        streak = self.get_streak()

        # Create cards
        self.create_stat_card(card_frame, "Total Habits", len(self.habits), "#6A1B9A")
        self.create_stat_card(card_frame, "Done Today", f"{done_today}/{total_today}", "#AB47BC")
        self.create_stat_card(card_frame, "Streak", f"{streak} days", "#FF6B35")

    def create_stat_card(self, parent, title, value, color):
        """Create a statistic card"""
        card = tk.Frame(parent, bg="white", width=220, height=120, 
                       relief="solid", bd=1)
        card.pack(side="left", padx=15)
        card.pack_propagate(False)
        
        tk.Label(card, text=title, font=("Times New Roman", 12, "bold"), 
                bg="white", fg=color).pack(pady=(20, 5))
        tk.Label(card, text=value, font=("Times New Roman", 24, "bold"), 
                bg="white", fg=color).pack()

    def get_streak(self):
        """Calculate current streak"""
        streak = 0
        check_date = date.today()
        
        while True:
            day_str = check_date.isoformat()
            scheduled = sum(1 for h in self.habits if check_date.weekday() in h.get("repeat_days", []))
            done = len([i for i in self.completed.get(day_str, [])])
            
            if scheduled > 0 and done == scheduled:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
                
        return streak

    def show_calendar(self):
        """Display the calendar view"""
        self.clear_content()
        
        # Title
        tk.Label(self.content, text="Your Habits Calendar", 
                font=self.fonts["heading"], fg=self.colors["text"], 
                bg=self.colors["background"]).pack(pady=10)

        # Calendar container
        main_frame = tk.Frame(self.content, bg=self.colors["background"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Month and year
        today = date.today()
        tk.Label(main_frame, text=today.strftime("%B %Y"), 
                font=("Times New Roman", 20, "bold"), 
                fg=self.colors["text"], bg=self.colors["background"]).pack(pady=10)

        # Create calendar grid
        self.create_calendar_grid(main_frame, today.year, today.month)

    def create_calendar_grid(self, parent, year, month):
        """Create the calendar grid with days"""
        cal_frame = tk.Frame(parent, bg=self.colors["background"])
        cal_frame.pack(fill="both", expand=True)

        # Configure grid
        for r in range(8):
            cal_frame.grid_rowconfigure(r, weight=1, minsize=80)
        for c in range(7):
            cal_frame.grid_columnconfigure(c, weight=1, minsize=100)

        # Weekday headers
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(weekdays):
            cell = tk.Frame(cal_frame, bg=self.colors["primary"], height=40, 
                           relief="raised", bd=1)
            cell.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            cell.grid_propagate(False)
            tk.Label(cell, text=day, font=("Times New Roman", 10, "bold"), 
                    fg="white", bg=self.colors["primary"]).place(relx=0.5, rely=0.5, anchor="center")

        # Days of month
        cal = calendar.monthcalendar(year, month)
        today = date.today()
        
        for week_num, week in enumerate(cal):
            row = week_num + 1
            for col, day in enumerate(week):
                if day == 0:
                    self.create_empty_cell(cal_frame, row, col)
                    continue
                    
                day_date = date(year, month, day)
                self.create_day_cell(cal_frame, row, col, day_date, today)

    def create_empty_cell(self, parent, row, col):
        """Create an empty calendar cell"""
        empty = tk.Frame(parent, bg=self.colors["background"], width=100, height=80)
        empty.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        empty.grid_propagate(False)

    def create_day_cell(self, parent, row, col, day_date, today):
        """Create a calendar cell for a specific day"""
        day_str = day_date.isoformat()
        weekday = day_date.weekday()

        # Get scheduled habits for this day
        scheduled_habits = []
        for i, h in enumerate(self.habits):
            if weekday in h.get("repeat_days", []):
                scheduled_habits.append((i, h))

        # Get completed habits
        completed_today = self.completed.get(day_str, [])
        done = len([i for i, h in scheduled_habits if i in completed_today])
        total = len(scheduled_habits)

        # Determine which categories have incomplete habits
        cats_with_incomplete = set()
        for i, h in scheduled_habits:
            if i not in completed_today:
                cats_with_incomplete.add(h["category"])

        # Determine background color
        bg = self.colors["background"]
        if day_date == today:
            bg = self.colors["highlight"]
        elif done == total and total > 0:
            bg = self.colors["completed"]

        # Create cell
        cell = tk.Frame(parent, bg=bg, relief="solid", bd=1, width=100, height=80)
        cell.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        cell.grid_propagate(False)

        # Day number
        day_label = tk.Label(cell, text=str(day_date.day), 
                           font=("Times New Roman", 11, "bold") if day_date == today else ("Times New Roman", 11), 
                           bg=bg, fg=self.colors["text"])
        day_label.place(x=8, y=8)

        # Category dots for incomplete habits
        if cats_with_incomplete:
            self.add_category_dots(cell, bg, cats_with_incomplete)

        # Completion indicator
        if scheduled_habits:
            self.add_completion_indicator(cell, bg, done, total)

        # Bind click event
        cell.bind("<Button-1>", lambda e, d=day_date: self.open_day(d))

    def add_category_dots(self, cell, bg, categories):
        """Add colored dots for habit categories"""
        dot_frame = tk.Frame(cell, bg=bg)
        dot_frame.place(relx=0.5, rely=0.8, anchor="center")
        
        for i, cat in enumerate(list(categories)[:4]):
            color = self.category_colors.get(cat, "#777")
            tk.Label(dot_frame, text="●", fg=color, font=("Times New Roman", 14), 
                    bg=bg).pack(side="left", padx=1)

    def add_completion_indicator(self, cell, bg, done, total):
        """Add completion indicator to cell"""
        dot_frame = cell.winfo_children()[0] if cell.winfo_children() else tk.Frame(cell, bg=bg)
        
        if 0 < done < total:
            tk.Label(dot_frame, text=f"✓{done}", font=("Times New Roman", 10), 
                    fg=self.colors["success"], bg=bg).pack(side="left", padx=2)
        elif done == total and total > 0:
            tk.Label(dot_frame, text="✓", font=("Times New Roman", 12, "bold"), 
                    fg=self.colors["success"], bg=bg).pack(side="left", padx=2)

    # ==================== ADD/EDIT HABIT ====================

    def show_add_habit(self):
        """Display the add/edit habit form"""
        self.clear_content()
        
        # Title based on mode
        title_text = "Edit Habit" if self.editing_index is not None else "Add New Habit"
        tk.Label(self.content, text=title_text, font=self.fonts["heading"], 
                fg=self.colors["text"], bg=self.colors["background"]).pack(pady=30)

        # Form container
        form = tk.Frame(self.content, bg=self.colors["background"])
        form.pack(pady=30)

        # Habit Type dropdown
        self.create_category_dropdown(form)

        # Task Name
        self.create_task_name_field(form)

        # Description
        self.create_description_field(form)

        # Color Legend
        self.create_color_legend(form)

        # Repeat Days
        self.create_repeat_days_section(form)

        # Save button
        button_text = "Update Habit" if self.editing_index is not None else "Add Habit"
        tk.Button(self.content, text=button_text, bg=self.colors["primary"], 
                fg="white", width=20, height=2, font=self.fonts["button"], 
                activebackground=self.colors["text"], 
                command=self.save_habit).pack(pady=40)

        # If editing, load existing data
        if self.editing_index is not None:
            self.load_habit_for_editing()

    def create_category_dropdown(self, parent):
        """Create category selection dropdown"""
        tk.Label(parent, text="Habit Type:", font=self.fonts["body"], 
                fg=self.colors["text"], bg=self.colors["background"]).grid(
                row=0, column=0, sticky="w", pady=10)
        
        categories = list(self.category_colors.keys())
        self.cat_var = tk.StringVar(value=categories[0])
        
        # Create dropdown menu
        self.category_menu = ttk.Combobox(parent, textvariable=self.cat_var, 
                                        values=categories, state="readonly",
                                        font=self.fonts["body"], width=30)
        self.category_menu.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    def create_task_name_field(self, parent):
        """Create task name entry field"""
        tk.Label(parent, text="Task Name:", font=self.fonts["body"], 
                fg=self.colors["text"], bg=self.colors["background"]).grid(
                row=1, column=0, sticky="w", pady=10)
        
        self.name_entry = tk.Entry(parent, width=40, font=self.fonts["body"], 
                                 bd=2, relief="groove")
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)

    def create_description_field(self, parent):
        """Create description text area"""
        tk.Label(parent, text="Description:", font=self.fonts["body"], 
                fg=self.colors["text"], bg=self.colors["background"]).grid(
                row=2, column=0, sticky="nw", pady=10)
        
        desc_frame = tk.Frame(parent, bg=self.colors["background"])
        desc_frame.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
        
        desc_scrollbar = tk.Scrollbar(desc_frame)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.desc_text = tk.Text(desc_frame, height=4, width=38, 
                               font=self.fonts["small"], bd=2, relief="groove",
                               yscrollcommand=desc_scrollbar.set, wrap=tk.WORD)
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.config(command=self.desc_text.yview)
        
        # Placeholder text
        self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
        self.desc_text.config(fg=self.colors["disabled"])
        
        # Bind focus events
        self.desc_text.bind("<FocusIn>", self.on_desc_focus_in)
        self.desc_text.bind("<FocusOut>", self.on_desc_focus_out)

    def create_color_legend(self, parent):
        """Create color legend for habit types"""
        legend_frame = tk.Frame(parent, bg=self.colors["background"])
        legend_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky="w")
        
        tk.Label(legend_frame, text="Color Legend:", 
                font=("Times New Roman", 10, "bold"), 
                fg=self.colors["text"], bg=self.colors["background"]).pack(side="left", padx=(0, 10))
        
        # Show first 4 colors
        sample_cats = list(self.category_colors.items())[:4]
        for category, color in sample_cats:
            legend_item = tk.Frame(legend_frame, bg=self.colors["background"])
            legend_item.pack(side="left", padx=5)
            tk.Label(legend_item, text="●", fg=color, 
                    font=("Times New Roman", 10), 
                    bg=self.colors["background"]).pack(side="left")
            tk.Label(legend_item, text=category, font=("Times New Roman", 8), 
                    fg=self.colors["text_light"], 
                    bg=self.colors["background"]).pack(side="left")

    def create_repeat_days_section(self, parent):
        """Create repeat days checkboxes"""
        tk.Label(parent, text="Repeat on:", font=("Times New Roman", 12, "bold"), 
                fg=self.colors["text"], bg=self.colors["background"]).grid(
                row=4, column=0, columnspan=2, pady=20)
        
        self.day_vars = []
        days_frame = tk.Frame(parent, bg=self.colors["background"])
        days_frame.grid(row=5, column=0, columnspan=2)
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.day_vars.append(var)
            
            cb_frame = tk.Frame(days_frame, bg=self.colors["background"])
            cb_frame.grid(row=0, column=i, padx=12)
            
            cb = tk.Checkbutton(cb_frame, variable=var, bg=self.colors["background"], 
                              activebackground=self.colors["background"], 
                              selectcolor="#E3FA72", highlightthickness=0)
            cb.pack(side="left")
            
            tk.Label(cb_frame, text=day, font=self.fonts["small"], 
                    fg=self.colors["text"], bg=self.colors["background"]).pack(side="left", padx=5)

    def on_desc_focus_in(self, event):
        """Handle focus in on description text"""
        if self.desc_text.get("1.0", "end-1c") == "Optional: Add details, notes, or motivation...":
            self.desc_text.delete("1.0", tk.END)
            self.desc_text.config(fg=self.colors["text"])

    def on_desc_focus_out(self, event):
        """Handle focus out on description text"""
        if not self.desc_text.get("1.0", "end-1c").strip():
            self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
            self.desc_text.config(fg=self.colors["disabled"])

    def load_habit_for_editing(self):
        """Load habit data into form for editing"""
        if self.editing_index is None or self.editing_index >= len(self.habits):
            return
            
        habit = self.habits[self.editing_index]
        
        # Set category
        self.cat_var.set(habit["category"])
        
        # Set task name
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, habit["name"])
        
        # Set description
        self.desc_text.delete("1.0", tk.END)
        if habit.get("description"):
            self.desc_text.insert("1.0", habit["description"])
            self.desc_text.config(fg=self.colors["text"])
        else:
            self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
            self.desc_text.config(fg=self.colors["disabled"])
        
        # Set day checkboxes
        for i, var in enumerate(self.day_vars):
            var.set(i in habit.get("repeat_days", []))

    def save_habit(self):
        """Save habit to database"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter task name!")
            return
            
        description = self.desc_text.get("1.0", "end-1c").strip()
        if description == "Optional: Add details, notes, or motivation...":
            description = ""
            
        days = [i for i, v in enumerate(self.day_vars) if v.get()]
        if not days:
            messagebox.showerror("Error", "Select at least one day!")
            return

        # Convert days to frequency string
        frequency = ",".join(str(d) for d in days)
        
        if self.editing_index is not None:
            # Update existing habit
            habit_id = self.habits[self.editing_index]["id"]
            try:
                db.update_habit(habit_id, name, description, frequency)
                # Update in-memory habit
                self.habits[self.editing_index].update({
                    "name": name,
                    "category": self.cat_var.get(),
                    "description": description,
                    "repeat_days": days
                })
                messagebox.showinfo("Success!", f"Updated: {self.cat_var.get()} - {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update habit: {e}")
                return
        else:
            # Add new habit
            try:
                habit_id = db.add_habit(self.user_id, name, description, frequency)
                self.habits.append({
                    "id": habit_id,
                    "name": name,
                    "category": self.cat_var.get(),
                    "description": description,
                    "repeat_days": days
                })
                messagebox.showinfo("Success!", f"Added: {self.cat_var.get()} - {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save habit: {e}")
                return
        
        # Reset form
        self.reset_habit_form()
        
        # Show calendar view
        self.show_calendar()

    def reset_habit_form(self):
        """Reset the habit form to default state"""
        self.name_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
        self.desc_text.config(fg=self.colors["disabled"])
        
        for var in self.day_vars:
            var.set(False)
        
        categories = list(self.category_colors.keys())
        self.cat_var.set(categories[0])
        
        self.editing_index = None

    # ==================== DAY VIEW ====================

    def open_day(self, day_date):
        """Open detailed view for a specific day"""
        popup = tk.Toplevel(self.dash)
        popup.title(day_date.strftime("%A, %B %d"))
        popup.geometry("400x520")
        popup.configure(bg=self.colors["background"])

        # Day header
        tk.Label(popup, text=day_date.strftime("%A\n%B %d, %Y"), 
                font=self.fonts["subheading"], fg=self.colors["text"], 
                bg=self.colors["background"]).pack(pady=30)

        # Get scheduled habits for this day
        weekday = day_date.weekday()
        day_str = day_date.isoformat()
        done = set(self.completed.get(day_str, []))
        scheduled = [i for i, h in enumerate(self.habits) 
                    if weekday in h.get("repeat_days", [])]

        if not scheduled:
            tk.Label(popup, text="No habits today!", fg=self.colors["primary"], 
                    font=self.fonts["body"], bg=self.colors["background"]).pack(pady=80)
            return

        # Progress summary
        completed_count = len([i for i in scheduled if i in done])
        total_count = len(scheduled)
        
        summary_frame = tk.Frame(popup, bg="#F0E8D8", relief="solid", bd=1)
        summary_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        tk.Label(summary_frame, text=f"Progress: {completed_count}/{total_count} completed", 
                font=("Times New Roman", 11, "bold"), fg=self.colors["text"], 
                bg="#F0E8D8").pack(pady=8)
        
        # Progress bar
        if total_count > 0:
            progress_width = 300
            progress_frame = tk.Frame(summary_frame, bg="#ddd", 
                                     height=8, width=progress_width)
            progress_frame.pack(pady=(0, 8))
            progress_frame.pack_propagate(False)
            
            completed_width = int((completed_count / total_count) * progress_width)
            progress_fill = tk.Frame(progress_frame, bg=self.colors["success"], 
                                    width=completed_width, height=8)
            progress_fill.place(x=0, y=0)

        # List habits
        for i in scheduled:
            self.create_day_habit_item(popup, i, day_str, done)

    def create_day_habit_item(self, parent, habit_index, day_str, done_set):
        """Create a habit item for day view"""
        habit = self.habits[habit_index]
        color = self.category_colors.get(habit["category"], "#666")
        is_done = habit_index in done_set
        
        frame = tk.Frame(parent, bg=self.colors["background"])
        frame.pack(pady=8, padx=20, fill="x")

        # Color dot
        tk.Label(frame, text="●", fg=color, font=("Times New Roman", 16), 
                bg=self.colors["background"]).pack(side="left")
        
        # Habit info
        info_frame = tk.Frame(frame, bg=self.colors["background"])
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Category
        category_label = tk.Label(info_frame, text=f"{habit['category']}: ", 
                                font=("Times New Roman", 12, "bold"), 
                                fg=self.colors["text"] if not is_done else self.colors["disabled"], 
                                bg=self.colors["background"])
        category_label.pack(anchor="w")
        
        # Habit name with optional strike-through
        task_text = f"  {habit['name']}"
        if is_done:
            # Create strike-through effect
            strike_frame = tk.Frame(info_frame, bg=self.colors["background"])
            strike_frame.pack(anchor="w")
            tk.Label(strike_frame, text=task_text, font=self.fonts["body"], 
                    fg=self.colors["disabled"], bg=self.colors["background"]).pack(side="left")
            line = tk.Frame(strike_frame, bg=self.colors["disabled"], height=1)
            line.place(in_=strike_frame, relx=0, rely=0.5, relwidth=1)
        else:
            tk.Label(info_frame, text=task_text, font=self.fonts["body"], 
                    fg=self.colors["text"], bg=self.colors["background"]).pack(anchor="w")

        # Toggle button
        btn_text = "Done" if is_done else "Mark Done"
        btn_color = self.colors["success"] if is_done else self.colors["primary"]
        tk.Button(frame, text=btn_text, bg=btn_color, fg="white", width=10,
                font=self.fonts["small"], activebackground=self.colors["text"],
                command=lambda idx=habit_index: self.toggle_day_completion(idx, day_str, parent)).pack(side="right")

    def toggle_day_completion(self, habit_index, day_str, popup):
        """Toggle completion status for a habit on a specific day"""
        self.completed.setdefault(day_str, [])
        habit_id = self.habits[habit_index]["id"]
        log_date = date.fromisoformat(day_str) if isinstance(day_str, str) else day_str
        
        if habit_index in self.completed[day_str]:
            # Remove completion
            self.completed[day_str].remove(habit_index)
            db.delete_habit_log(self.user_id, habit_id, log_date)
        else:
            # Add completion
            self.completed[day_str].append(habit_index)
            db.add_habit_log(self.user_id, habit_id, log_date, "completed")
        
        popup.destroy()
        self.show_calendar()

    # ==================== VIEW HABITS ====================

    def show_view_habits(self):
        """Display all habits in a list view"""
        self.clear_content()
        
        tk.Label(self.content, text="Your Habits", font=self.fonts["heading"], 
                fg=self.colors["text"], bg=self.colors["background"]).pack(pady=30)
        
        if not self.habits:
            tk.Label(self.content, text="No habits added yet!", 
                    font=self.fonts["body"], fg=self.colors["primary"], 
                    bg=self.colors["background"]).pack(pady=50)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(self.content, bg=self.colors["background"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["background"])
        
        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Display habits
        for idx, habit in enumerate(self.habits):
            self.create_habit_card(scrollable_frame, idx, habit)

    def create_habit_card(self, parent, index, habit):
        """Create a card for a habit in the view"""
        main_frame = tk.Frame(parent, bg="#F0E8D8", relief="solid", bd=1)
        main_frame.pack(fill="x", padx=20, pady=8)
        
        # Top row with habit info
        top_frame = tk.Frame(main_frame, bg="#F0E8D8")
        top_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # Category color dot
        color = self.category_colors.get(habit["category"], "#666")
        tk.Label(top_frame, text="●", fg=color, font=("Times New Roman", 16), 
                bg="#F0E8D8").pack(side="left")
        
        # Habit name and category
        tk.Label(top_frame, text=f"{habit['category']}: {habit['name']}", 
                font=self.fonts["card_title"], fg=self.colors["text"], 
                bg="#F0E8D8").pack(side="left", padx=5, fill="x", expand=True)
        
        # Days abbreviation
        days = "".join(["MTWTFSS"[d] for d in habit["repeat_days"]])
        tk.Label(top_frame, text=days, fg=self.colors["secondary"], 
                font=self.fonts["small"], bg="#F0E8D8").pack(side="left", padx=10)
        
        # Action buttons
        button_frame = tk.Frame(top_frame, bg="#F0E8D8")
        button_frame.pack(side="right")
        
        # Edit button
        edit_btn = tk.Button(button_frame, text="✏ Edit", font=self.fonts["small"], 
                          bg=self.colors["success"], fg="white", width=8, height=1,
                          command=lambda idx=index: self.edit_habit(idx))
        edit_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = tk.Button(button_frame, text="🗑 Delete", font=self.fonts["small"], 
                            bg=self.colors["error"], fg="white", width=8, height=1,
                            command=lambda idx=index: self.delete_habit(idx))
        delete_btn.pack(side="left", padx=2)
        
        # Description (if exists)
        if habit.get("description"):
            desc_frame = tk.Frame(main_frame, bg="#F0E8D8")
            desc_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            tk.Label(desc_frame, text="📝", font=self.fonts["small"], 
                    bg="#F0E8D8").pack(side="left")
            tk.Label(desc_frame, text=habit["description"], font=self.fonts["small"], 
                    fg=self.colors["text_light"], bg="#F0E8D8", 
                    wraplength=700, justify="left").pack(side="left", padx=5)

    def edit_habit(self, index):
        """Switch to edit mode for a habit"""
        self.editing_index = index
        self.show_add_habit()

    def delete_habit(self, index):
        """Delete a habit after confirmation"""
        if 0 <= index < len(self.habits):
            habit_name = self.habits[index]["name"]
            habit_id = self.habits[index]["id"]
            
            if messagebox.askyesno("Delete Habit", 
                                 f"Are you sure you want to delete '{habit_name}'?\n\n"
                                 "This will also remove all completion records for this habit."):
                # Delete from database
                try:
                    db.delete_habit(habit_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete habit: {e}")
                    return
                
                # Remove from memory
                self.remove_habit_from_memory(index)
                
                messagebox.showinfo("Success!", f"Deleted habit: {habit_name}")
                self.show_view_habits()

    def remove_habit_from_memory(self, index):
        """Remove habit from in-memory data structures"""
        # Remove completion records
        for day_str in list(self.completed.keys()):
            if index in self.completed[day_str]:
                self.completed[day_str].remove(index)
            # Remove empty days
            if not self.completed[day_str]:
                del self.completed[day_str]
        
        # Adjust indices for other habits
        for day_str in self.completed:
            self.completed[day_str] = [
                i-1 if i > index else i 
                for i in self.completed[day_str]
                if i != index
            ]
        
        # Remove the habit
        del self.habits[index]

    # ==================== MOOD PICKER ====================

    def open_mood_picker(self):
        """Open mood selection popup"""
        popup = tk.Toplevel(self.dash)
        popup.geometry("350x450")
        popup.title("Mood")
        popup.configure(bg=self.colors["background"])
        
        tk.Label(popup, text="How are you today?", font=self.fonts["subheading"], 
                fg=self.colors["text"], bg=self.colors["background"]).pack(pady=30)

        moods = [
            ("😊 Happy", "Happy"),
            ("😢 Sad", "Sad"),
            ("🎉 Excited", "Excited"),
            ("😌 Calm", "Calm"),
            ("😴 Tired", "Tired"),
            ("😠 Angry", "Angry")
        ]
        
        for emoji, mood in moods:
            btn = tk.Button(popup, text=emoji, font=("Times New Roman", 16), 
                          bg=self.colors["secondary"], fg="white", 
                          width=8, height=1, activebackground=self.colors["text"],
                          command=lambda m=mood: self.set_mood(m, popup))
            btn.pack(pady=6)

    def set_mood(self, mood, popup):
        """Set and save user's mood"""
        popup.destroy()
        self.current_mood = mood
        self.mood_label.config(text=f"Today's Mood: {mood}", fg=self.colors["text"])
        
        # Save to database
        try:
            db.add_mood_entry(self.user_id, mood)
        except Exception as e:
            print(f"Error saving mood: {e}")

    # ==================== LOGOUT ====================

    def logout(self):
        """Handle user logout"""
        if messagebox.askyesno("Logout", "Leave HabitMate?"):
            self.dash.destroy()
            self.root.deiconify()


if __name__ == "_main_":
    root = tk.Tk()
    app = HabitMateApp(root)
    root.mainloop()