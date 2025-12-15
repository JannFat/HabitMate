# habitmate_final_WITH_REGISTRATION_UI.py - REGISTRATION UI READY FOR DATABASE
import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
import calendar
import random
# near other imports
import database as db   # uses the database.py file


class HabitMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HabitMate")
        self.root.geometry("1020x720")
        self.root.resizable(True, True)

        self.category_colors = {
            "Health": "#69E136", "Study": "#2196F3", "Fitness": "#9D3D23",
            "Work": "#9C27B0", "Personal": "#FF9800", "Mindfulness": "#00BCD4", "Social": "#E91E63"
        }

        # Single user system for now (will be replaced with database)
        self.habits = []
        self.completed = {}
        
        # For editing habits
        self.editing_index = None
        
        # Store logo images
        self.login_logo = None
        self.sidebar_logo = None

        self.build_login_screen()
    def load_user_logs(self):
        """
        Loads completion logs from DB and fills self.completed.
        Maps: 'YYYY-MM-DD' -> [habitIndex]
        """
        self.completed = {}
        if not hasattr(self, "user_id"):
            return

        logs = db.get_habit_logs(self.user_id)

        # Create habit_id -> habit_index mapping
        habit_index_map = {}
        for index, h in enumerate(self.habits):
            if "id" in h:
                habit_index_map[h["id"]] = index

        # Populate self.completed
        for habit_id, log_date in logs:
            log_date = log_date.isoformat()

            if habit_id not in habit_index_map:
                continue  # skip if habit not loaded or deleted

        index = habit_index_map[habit_id]
        self.completed.setdefault(log_date, [])

        if index not in self.completed[log_date]:
            self.completed[log_date].append(index)

    def build_login_screen(self):
        for w in self.root.winfo_children(): 
            w.destroy()
            
        self.root.configure(bg="#FBF5E5")
        
        # Create main container
        container = tk.Frame(self.root, bg="#FBF5E5")
        container.pack(fill="both", expand=True)
        
        # Shadow effect
        shadow = tk.Frame(container, bg="#dddddd", width=430, height=530)
        shadow.place(relx=0.5, rely=0.5, anchor="center")
        shadow.pack_propagate(False)
        
        # White card
        card = tk.Frame(container, bg="white", width=420, height=520)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        # Load logo for login screen
        try:
            self.login_logo = tk.PhotoImage(file="HM_logo.png").subsample(6, 6)  # Adjust subsample as needed
            logo_frame = tk.Frame(card, bg="white", height=60)  # Reduced height from 80
            logo_frame.pack(pady=(15, 5), fill="x")  # Reduced padding: (15, 5) instead of (30, 15)
            
            logo_label = tk.Label(logo_frame, image=self.login_logo, bg="white")
            logo_label.pack()
        except Exception as e:
            # If logo not found, create a text placeholder
            logo_frame = tk.Frame(card, bg="white", height=50)
            logo_frame.pack(pady=(15, 5), fill="x")
            tk.Label(logo_frame, text="⚪ HM", font=("Times New Roman", 24, "bold"), 
                    fg="#C89047", bg="white").pack()
        
        # Title
        title_frame = tk.Frame(card, bg="white")
        title_frame.pack(pady=(5, 25))  # Reduced from (0, 30) to (5, 25)
        
        tk.Label(title_frame, text="HABITMATE", font=("Segoe UI", 28, "bold"), 
                fg="#212121", bg="white").pack()
        tk.Label(title_frame, text="Calendar Habit Tracker", font=("Segoe UI", 12), 
                fg="#C89047", bg="white").pack(pady=(3, 0))  # Reduced from (5, 0)
        
        # Form container
        form_container = tk.Frame(card, bg="white")
        form_container.pack(fill="both", expand=True, padx=50)
        
        # Username
        username_frame = tk.Frame(form_container, bg="white")
        username_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(username_frame, text="Username", font=("Segoe UI", 11), 
                fg="#555", bg="white").pack(anchor="w")
        
        self.login_username = tk.Entry(username_frame, width=30, font=("Segoe UI", 11), 
                                    bd=0, relief="flat", highlightthickness=2,
                                    highlightbackground="#ddd", highlightcolor="#C89047")
        self.login_username.pack(fill="x", pady=(8, 0), ipady=8)
        self.login_username.insert(0, "admin")
        self.login_username.focus()
        
        # Password with eye icon
        password_frame = tk.Frame(form_container, bg="white")
        password_frame.pack(fill="x", pady=(0, 35))
        
        tk.Label(password_frame, text="Password", font=("Segoe UI", 11), 
                fg="#555", bg="white").pack(anchor="w")
        
        pwd_entry_frame = tk.Frame(password_frame, bg="white")
        pwd_entry_frame.pack(fill="x", pady=(8, 0))
        
        self.login_password = tk.Entry(pwd_entry_frame, width=30, font=("Segoe UI", 11), 
                                    show="●", bd=0, relief="flat",
                                    highlightthickness=2, highlightbackground="#ddd", 
                                    highlightcolor="#C89047")
        self.login_password.pack(side="left", fill="x", expand=True, ipady=8)
        self.login_password.insert(0, "123")
        
        eye_btn = tk.Button(pwd_entry_frame, text="👁", font=("Segoe UI", 12), 
                        bg="white", fg="#666", bd=0, cursor="hand2",
                        activebackground="#f0f0f0", command=self.toggle_login_password)
        eye_btn.pack(side="right", padx=(10, 0))
        self.login_eye_btn = eye_btn
        
        # Login Button
        button_frame = tk.Frame(form_container, bg="white")
        button_frame.pack(pady=(0, 20))
        
        tk.Button(button_frame, text="Login", bg="#C89047", fg="white", 
                font=("Segoe UI", 12, "bold"), width=16, height=1,
                bd=0, cursor="hand2", command=self.login).pack()
        
        # Register link
        link_frame = tk.Frame(form_container, bg="white")
        link_frame.pack()
        
        tk.Label(link_frame, text="Don't have an account?", fg="#555", 
                bg="white", font=("Segoe UI", 10)).pack(side="left")
        
        create_link = tk.Label(link_frame, text="Create one", fg="#C89047", 
                            bg="white", font=("Segoe UI", 10, "underline"),
                            cursor="hand2")
        create_link.pack(side="left", padx=5)
        create_link.bind("<Button-1>", lambda e: self.show_register_screen())

    def toggle_login_password(self):
        """Toggle visibility of login password"""
        if self.login_password.cget("show") == "●":
            self.login_password.config(show="")
            self.login_eye_btn.config(text="🔒")
        else:
            self.login_password.config(show="●")
            self.login_eye_btn.config(text="👁")

    def toggle_register_password(self, entry, button):
        """Toggle visibility of register password"""
        if entry.cget("show") == "●":
            entry.config(show="")
            button.config(text="🔒")
        else:
            entry.config(show="●")
            button.config(text="👁")

    def show_register_screen(self):
        for w in self.root.winfo_children(): 
            w.destroy()
            
        self.root.configure(bg="#FBF5E5")
        
        # Create main container
        container = tk.Frame(self.root, bg="#FBF5E5")
        container.pack(fill="both", expand=True)
        
        # Shadow + Card
        shadow = tk.Frame(container, bg="#dddddd", width=440, height=600)
        shadow.place(relx=0.5, rely=0.5, anchor="center")
        shadow.pack_propagate(False)
        
        card = tk.Frame(container, bg="white", width=430, height=590)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        # Title (NO LOGO on register screen)
        title_frame = tk.Frame(card, bg="white")
        title_frame.pack(pady=(50, 40))
        
        tk.Label(title_frame, text="CREATE ACCOUNT", font=("Segoe UI", 28, "bold"), 
                fg="#212121", bg="white").pack()
        tk.Label(title_frame, text="Join HabitMate to track your habits", 
                font=("Segoe UI", 12), fg="#C89047", bg="white").pack(pady=(5, 0))
        
        # Form container
        form_container = tk.Frame(card, bg="white")
        form_container.pack(fill="both", expand=True, padx=60)
        
        # Username
        username_frame = tk.Frame(form_container, bg="white")
        username_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(username_frame, text="Username", font=("Segoe UI", 11), 
                fg="#555", bg="white").pack(anchor="w")
        
        self.register_username = tk.Entry(username_frame, width=30, font=("Segoe UI", 11), 
                                        bd=0, relief="flat", highlightthickness=2,
                                        highlightbackground="#ddd", highlightcolor="#C89047")
        self.register_username.pack(fill="x", pady=(8, 0), ipady=8)
        self.register_username.focus()
        
        # Password
        password_frame = tk.Frame(form_container, bg="white")
        password_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(password_frame, text="Password", font=("Segoe UI", 11), 
                fg="#555", bg="white").pack(anchor="w")
        
        pwd_entry_frame1 = tk.Frame(password_frame, bg="white")
        pwd_entry_frame1.pack(fill="x", pady=(8, 0))
        
        self.register_password = tk.Entry(pwd_entry_frame1, width=30, font=("Segoe UI", 11), 
                                        show="●", bd=0, relief="flat",
                                        highlightthickness=2, highlightbackground="#ddd", 
                                        highlightcolor="#C89047")
        self.register_password.pack(side="left", fill="x", expand=True, ipady=8)
        
        eye1 = tk.Button(pwd_entry_frame1, text="👁", font=("Segoe UI", 12), 
                        bg="white", fg="#666", bd=0, cursor="hand2",
                        activebackground="#f0f0f0",
                        command=lambda: self.toggle_register_password(self.register_password, eye1))
        eye1.pack(side="right", padx=(10, 0))
        self.register_eye_btn1 = eye1
        
        # Confirm Password
        confirm_frame = tk.Frame(form_container, bg="white")
        confirm_frame.pack(fill="x", pady=(0, 35))
        
        tk.Label(confirm_frame, text="Confirm Password", font=("Segoe UI", 11), 
                fg="#555", bg="white").pack(anchor="w")
        
        pwd_entry_frame2 = tk.Frame(confirm_frame, bg="white")
        pwd_entry_frame2.pack(fill="x", pady=(8, 0))
        
        self.register_confirm_password = tk.Entry(pwd_entry_frame2, width=30, font=("Segoe UI", 11), 
                                                show="●", bd=0, relief="flat",
                                                highlightthickness=2, highlightbackground="#ddd", 
                                                highlightcolor="#C89047")
        self.register_confirm_password.pack(side="left", fill="x", expand=True, ipady=8)
        
        eye2 = tk.Button(pwd_entry_frame2, text="👁", font=("Segoe UI", 12), 
                        bg="white", fg="#666", bd=0, cursor="hand2",
                        activebackground="#f0f0f0",
                        command=lambda: self.toggle_register_password(self.register_confirm_password, eye2))
        eye2.pack(side="right", padx=(10, 0))
        self.register_eye_btn2 = eye2
        
        # Register Button
        button_frame = tk.Frame(form_container, bg="white")
        button_frame.pack(pady=(0, 20))
        
        tk.Button(button_frame, text="Register", bg="#C89047", fg="white", 
                font=("Segoe UI", 12, "bold"), width=20, height=2,
                bd=0, cursor="hand2", command=self.register).pack()
        
        # Login link
        link_frame = tk.Frame(form_container, bg="white")
        link_frame.pack()
        
        tk.Label(link_frame, text="Already have an account?", fg="#555", 
                bg="white", font=("Segoe UI", 10)).pack(side="left")
        
        login_link = tk.Label(link_frame, text="Login here", fg="#C89047", 
                            bg="white", font=("Segoe UI", 10, "underline"),
                            cursor="hand2")
        login_link.pack(side="left", padx=5)
        login_link.bind("<Button-1>", lambda e: self.build_login_screen())
    
    def load_user_data(self):
        """
        Loads habits (and optionally completed logs) from DB for self.user_id.
        Converts DB rows into the in-memory structure the GUI expects.
        """
        self.habits = []
        self.completed = {}

        try:
            rows = db.get_habits(self.user_id)  # rows: list of tuples
            # Expected row columns: (habit_id, title, description, frequency, created_at)
            for row in rows:
                habit_id = row[0]
                title = row[1]
                description = row[2] or ""
                frequency = row[3] or ""  # adapt depending on how you store frequency/repeat_days
                # IMPORTANT: gui expects "repeat_days" as list of weekday indices.
                # If your DB stores frequency as CSV of day indices ("0,1,2") parse that here.
                # For example, if frequency column stores "0,2,4":
                repeat_days = []
                if frequency:
                    # Try parsing CSV of ints
                    try:
                        repeat_days = [int(x) for x in str(frequency).split(",") if x.strip().isdigit()]
                    except Exception:
                        repeat_days = []

                habit_dict = {
                    "id": habit_id,
                    "name": title,
                    "category": "Personal",   # adjust if you stored category in DB
                    "description": description,
                    "repeat_days": repeat_days
                }
                self.habits.append(habit_dict)
            
            self.load_user_logs()

            # (Optional) load completion logs from habit_logs table and fill self.completed
            # You can implement db.get_habit_logs(user_id) that returns (habit_id, log_date)
            # and then transform into self.completed[date_iso] = [list of habit indices]
        except Exception as e:
            print("Error loading user data:", e)



    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        # Call DB login
        success, user_id = db.login_user(username, password)
        if success:
            self.user_id = user_id
            # Load user-specific data (habits/completed)
            self.load_user_data()
            self.root.withdraw()
            self.open_dashboard()
        else:
            messagebox.showinfo("Login Failed", "Invalid credentials!")

    def register(self):
        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()

        # Basic validation
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Call DB register
        success, message = db.register_user(username, password)
        if success:
            messagebox.showinfo("Registration Successful", message)
            self.build_login_screen()
        else:
            messagebox.showerror("Registration Failed", message)


    def open_dashboard(self):
        self.dash = tk.Toplevel(self.root)
        self.dash.title("HabitMate")
        self.dash.geometry("1020x720")
        self.dash.configure(bg="#FBF5E5")

        sidebar = tk.Frame(self.dash, bg="#A35C7A", width=220)
        sidebar.pack(side="left", fill="y")

        # Sidebar Logo at the top
        try:
            self.sidebar_logo = tk.PhotoImage(file="HM_logo.png").subsample(4, 4)  # Adjust size
            logo_sidebar = tk.Label(sidebar, image=self.sidebar_logo, bg="#A35C7A")
            logo_sidebar.image = self.sidebar_logo  # Keep reference
            logo_sidebar.pack(pady=(20, 5))  # Reduced from (25, 10)
        except Exception as e:
            # Text placeholder if logo not found
            logo_frame = tk.Frame(sidebar, bg="#A35C7A", height=50)  # Reduced height
            logo_frame.pack(pady=(20, 5), fill="x")
            tk.Label(logo_frame, text="⚪ HM", font=("Times New Roman", 20, "bold"), 
                    fg="white", bg="#A35C7A").pack()

        # App name below logo
        tk.Label(sidebar, text="HabitMate", bg="#A35C7A", fg="white",
                 font=("Times New Roman", 16, "bold")).pack(pady=(0, 20))  # Reduced from (0, 25)

        buttons = ["Home", "Calendar", "Add Habit", "View Habits", "Mood", "Logout"]
        commands = [self.show_home, self.show_calendar, self.show_add_habit, 
                self.show_view_habits, self.open_mood_picker, self.logout]
        
        for text, cmd in zip(buttons, commands):
            bg_color = "#C45C3D" if text == "Logout" else "#C89047"
            tk.Button(sidebar, text=text, width=20, height=2, bg=bg_color, 
                    fg="white", font=("Times New Roman", 10, "bold"), command=cmd).pack(pady=8, padx=10)

        self.content = tk.Frame(self.dash, bg="#FBF5E5")
        self.content.pack(side="right", fill="both", expand=True)

        self.mood_label = tk.Label(self.content, text="Today's Mood: Not set", 
                                font=("Times New Roman", 12), fg="#212121", bg="#FBF5E5")
        self.mood_label.pack(anchor="ne", padx=20, pady=10)

        self.show_home()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content, text="Welcome Back!", font=("Times New Roman", 26, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(pady=30)

        quotes = ["Small steps every day", "Consistency compounds", "You're building something great", "Keep going!"]
        tk.Label(self.content, text=random.choice(quotes), font=("Times New Roman", 14, "italic"), 
                fg="#C89047", bg="#FBF5E5").pack(pady=10)

        card_frame = tk.Frame(self.content, bg="#FBF5E5")
        card_frame.pack(pady=20)

        def card(title, value, color):
            c = tk.Frame(card_frame, bg="white", width=220, height=120, relief="solid", bd=1)
            c.pack(side="left", padx=15); c.pack_propagate(False)
            tk.Label(c, text=title, font=("Times New Roman", 12, "bold"), bg="white", fg=color).pack(pady=(20,5))
            tk.Label(c, text=value, font=("Times New Roman", 24, "bold"), bg="white", fg=color).pack()

        today_str = date.today().isoformat()
        done_today = len(self.completed.get(today_str, []))
        total_today = sum(1 for h in self.habits if date.today().weekday() in h.get("repeat_days", []))

        card("Total Habits", len(self.habits), "#6A1B9A")
        card("Done Today", f"{done_today}/{total_today}", "#AB47BC")
        card("Streak", f"{self.get_streak()} days", "#FF6B35")

    def get_streak(self):
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
        self.clear_content()
        tk.Label(self.content, text="Your Habits Calendar", font=("Times New Roman", 24, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(pady=10)

        today = date.today()
        year, month = today.year, today.month

        main_frame = tk.Frame(self.content, bg="#FBF5E5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(main_frame, text=today.strftime("%B %Y"), font=("Times New Roman", 20, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(pady=10)

        cal_frame = tk.Frame(main_frame, bg="#FBF5E5")
        cal_frame.pack(fill="both", expand=True)

        for r in range(8):
            cal_frame.grid_rowconfigure(r, weight=1, minsize=80)
        for c in range(7):
            cal_frame.grid_columnconfigure(c, weight=1, minsize=100)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(weekdays):
            cell = tk.Frame(cal_frame, bg="#C89047", height=40, relief="raised", bd=1)
            cell.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            cell.grid_propagate(False)
            tk.Label(cell, text=day, font=("Times New Roman", 10, "bold"), 
                    fg="white", bg="#C89047").place(relx=0.5, rely=0.5, anchor="center")

        cal = calendar.monthcalendar(year, month)
        for week_num, week in enumerate(cal):
            row = week_num + 1
            for col, day in enumerate(week):
                if day == 0:
                    empty = tk.Frame(cal_frame, bg="#FBF5E5", width=100, height=80)
                    empty.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                    empty.grid_propagate(False)
                    continue

                day_date = date(year, month, day)
                day_str = day_date.isoformat()
                weekday = day_date.weekday()

                # Find scheduled habits for this day
                scheduled_habits = []
                for i, h in enumerate(self.habits):
                    if weekday in h.get("repeat_days", []):
                        scheduled_habits.append((i, h))

                # Calculate which habits are completed
                completed_today = self.completed.get(day_str, [])
                
                # Calculate completion status for cell color
                done = len([i for i, h in scheduled_habits if i in completed_today])
                total = len(scheduled_habits)

                # Determine which categories to show dots for (only INCOMPLETE habits)
                cats_with_incomplete = set()
                for i, h in scheduled_habits:
                    if i not in completed_today:  # Only show dot for incomplete habits
                        cats_with_incomplete.add(h["category"])

                bg = "#FBF5E5"
                if day_date == today:
                    bg = "#FFF59D"
                elif done == total and total > 0:
                    bg = "#C8E6C9"  # Green for fully completed day

                cell = tk.Frame(cal_frame, bg=bg, relief="solid", bd=1, width=100, height=80)
                cell.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                cell.grid_propagate(False)

                tk.Label(cell, text=str(day), 
                        font=("Times New Roman", 11, "bold") if day_date == today else ("Times New Roman", 11), 
                        bg=bg, fg="#212121").place(x=8, y=8)

                # Show dots only for categories with INCOMPLETE habits
                if cats_with_incomplete:
                    dot_frame = tk.Frame(cell, bg=bg)
                    dot_frame.place(relx=0.5, rely=0.8, anchor="center")
                    for i, cat in enumerate(list(cats_with_incomplete)[:4]):
                        color = self.category_colors.get(cat, "#777")
                        tk.Label(dot_frame, text="●", fg=color, font=("Times New Roman", 14), bg=bg).pack(side="left", padx=1)
                    
                    # Show completion indicator if some habits are done
                    if done > 0 and done < total:
                        tk.Label(dot_frame, text=f"✓{done}", font=("Times New Roman", 10), fg="#4CAF50", bg=bg).pack(side="left", padx=2)
                    elif done == total and total > 0:
                        tk.Label(dot_frame, text="✓", font=("Times New Roman", 12, "bold"), fg="#4CAF50", bg=bg).pack(side="left", padx=2)

                cell.bind("<Button-1>", lambda e, d=day_date: self.open_day(d))

    def open_day(self, day_date):
        popup = tk.Toplevel(self.dash)
        popup.title(day_date.strftime("%A, %B %d"))
        popup.geometry("400x520")
        popup.configure(bg="#FBF5E5")

        tk.Label(popup, text=day_date.strftime("%A\n%B %d, %Y"), 
                font=("Times New Roman", 16, "bold"), fg="#212121", bg="#FBF5E5").pack(pady=30)

        weekday = day_date.weekday()
        day_str = day_date.isoformat()
        done = set(self.completed.get(day_str, []))

        scheduled = [i for i, h in enumerate(self.habits) if weekday in h.get("repeat_days", [])]

        if not scheduled:
            tk.Label(popup, text="No habits today!", fg="#C89047", 
                    font=("Times New Roman", 14), bg="#FBF5E5").pack(pady=80)
            return

        # Add summary at the top
        summary_frame = tk.Frame(popup, bg="#F0E8D8", relief="solid", bd=1)
        summary_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        completed_count = len([i for i in scheduled if i in done])
        total_count = len(scheduled)
        
        tk.Label(summary_frame, text=f"Progress: {completed_count}/{total_count} completed", 
                font=("Times New Roman", 11, "bold"), fg="#212121", bg="#F0E8D8").pack(pady=8)
        
        # Progress bar
        if total_count > 0:
            progress_width = 300
            progress_frame = tk.Frame(summary_frame, bg="#ddd", height=8, width=progress_width)
            progress_frame.pack(pady=(0, 8))
            progress_frame.pack_propagate(False)
            
            completed_width = int((completed_count / total_count) * progress_width)
            progress_fill = tk.Frame(progress_frame, bg="#4CAF50", width=completed_width, height=8)
            progress_fill.place(x=0, y=0)

        for i in scheduled:
            h = self.habits[i]
            color = self.category_colors.get(h["category"], "#666")
            is_done = i in done
            status = "Done" if is_done else "Mark Done"
            btn_color = "#4CAF50" if is_done else "#C89047"
            text_color = "#888" if is_done else "#212121"

            f = tk.Frame(popup, bg="#FBF5E5")
            f.pack(pady=8, padx=20, fill="x")

            # Dot indicator
            tk.Label(f, text="●", fg=color, font=("Times New Roman", 16), bg="#FBF5E5").pack(side="left")
            
            # Habit info with strike-through if done
            info_frame = tk.Frame(f, bg="#FBF5E5")
            info_frame.pack(side="left", fill="x", expand=True)
            
            # Category name
            category_label = tk.Label(info_frame, text=f"{h['category']}: ", 
                                    font=("Times New Roman", 12, "bold"), fg=text_color, bg="#FBF5E5")
            category_label.pack(anchor="w")
            if is_done:
                category_label.config(fg="#888")
            
            # Task name with optional strike-through
            task_text = f"  {h['name']}"
            if is_done:
                # Create strike-through effect
                strike_frame = tk.Frame(info_frame, bg="#FBF5E5")
                strike_frame.pack(anchor="w")
                tk.Label(strike_frame, text=task_text, font=("Times New Roman", 12), 
                        fg="#888", bg="#FBF5E5").pack(side="left")
                # Draw a line through the text
                line = tk.Frame(strike_frame, bg="#888", height=1)
                line.place(in_=strike_frame, relx=0, rely=0.5, relwidth=1)
            else:
                tk.Label(info_frame, text=task_text, font=("Times New Roman", 12), 
                        fg="#212121", bg="#FBF5E5").pack(anchor="w")

            tk.Button(f, text=status, bg=btn_color, fg="white", width=10,
                    font=("Times New Roman", 10), activebackground="#212121",
                    command=lambda idx=i: self.toggle_day(idx, day_str, popup)).pack(side="right")

    def toggle_day(self, idx, day_str, popup):
        habit_id = self.habits[idx].get("id")

        # If marking as done
        if idx not in self.completed.get(day_str, []):
            db.add_habit_log(self.user_id, habit_id, "done")
            self.completed.setdefault(day_str, []).append(idx)
        else:
            # Optional: Remove log from DB (if you want delete function)
            # db.delete_habit_log(self.user_id, habit_id, day_str)
            self.completed[day_str].remove(idx)

        if not self.completed[day_str]:
            del self.completed[day_str]

        popup.destroy()
        self.show_calendar()

    def show_add_habit(self):
        self.clear_content()
        self.editing_index = None  # Reset editing mode
        
        title_text = "Add New Habit" if self.editing_index is None else "Edit Habit"
        tk.Label(self.content, text=title_text, font=("Times New Roman", 22, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(pady=30)

        form = tk.Frame(self.content, bg="#FBF5E5")
        form.pack(pady=30)

        # Habit Type with color indicators
        tk.Label(form, text="Habit Type:", font=("Times New Roman", 12), 
                fg="#212121", bg="#FBF5E5").grid(row=0, column=0, sticky="w", pady=10)
        cats = list(self.category_colors.keys())
        self.cat_var = tk.StringVar(value=cats[0])
        
        # Create custom dropdown with colored options
        menu_button = tk.Menubutton(form, text="Select Habit Type", bg="white", fg="#212121", 
                                font=("Times New Roman", 10), relief="groove", bd=2,
                                width=33, anchor="w", direction="below")
        menu_button.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        
        # Create the menu
        category_menu = tk.Menu(menu_button, tearoff=0, bg="white", fg="#212121", font=("Times New Roman", 10))
        menu_button.config(menu=category_menu)
        
        # Function to update the menu button text
        def set_category(category):
            self.cat_var.set(category)
            menu_button.config(text=f"  ●  {category}")
        
        # Add colored options to the menu
        for category in cats:
            color = self.category_colors.get(category, "#777")
            # Create a special menu item with colored dot
            category_menu.add_command(
                label=f"  ●  {category}",
                command=lambda c=category: set_category(c),
                foreground=color,
                background="white",
                activebackground="#F0E8D8",
                activeforeground=color,
                font=("Times New Roman", 10)
            )
        
        # Set initial text
        set_category(cats[0])

        # Task Name
        tk.Label(form, text="Task Name:", font=("Times New Roman", 12), 
                fg="#212121", bg="#FBF5E5").grid(row=1, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(form, width=40, font=("Times New Roman", 11), bd=2, relief="groove")
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)

        # Description Box
        tk.Label(form, text="Description:", font=("Times New Roman", 12), 
                fg="#212121", bg="#FBF5E5").grid(row=2, column=0, sticky="nw", pady=10)
        
        desc_frame = tk.Frame(form, bg="#FBF5E5")
        desc_frame.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
        
        desc_scrollbar = tk.Scrollbar(desc_frame)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.desc_text = tk.Text(desc_frame, height=4, width=38, font=("Times New Roman", 10), 
                                bd=2, relief="groove", yscrollcommand=desc_scrollbar.set,
                                wrap=tk.WORD)
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.config(command=self.desc_text.yview)
        
        self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
        self.desc_text.config(fg="#888")
        
        def on_desc_focus_in(event):
            if self.desc_text.get("1.0", "end-1c") == "Optional: Add details, notes, or motivation...":
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.config(fg="#212121")
        
        def on_desc_focus_out(event):
            if not self.desc_text.get("1.0", "end-1c").strip():
                self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
                self.desc_text.config(fg="#888")
        
        self.desc_text.bind("<FocusIn>", on_desc_focus_in)
        self.desc_text.bind("<FocusOut>", on_desc_focus_out)

        # Color Legend for habit types
        legend_frame = tk.Frame(form, bg="#FBF5E5")
        legend_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky="w")
        
        tk.Label(legend_frame, text="Color Legend:", font=("Times New Roman", 10, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(side="left", padx=(0, 10))
        
        # Show first 4 colors as examples
        sample_cats = list(self.category_colors.items())[:4]
        for category, color in sample_cats:
            legend_item = tk.Frame(legend_frame, bg="#FBF5E5")
            legend_item.pack(side="left", padx=5)
            tk.Label(legend_item, text="●", fg=color, font=("Times New Roman", 10), bg="#FBF5E5").pack(side="left")
            tk.Label(legend_item, text=category, font=("Times New Roman", 8), fg="#666", bg="#FBF5E5").pack(side="left")

        # Repeat Days Section
        tk.Label(form, text="Repeat on:", font=("Times New Roman", 12, "bold"), 
                fg="#212121", bg="#FBF5E5").grid(row=4, column=0, columnspan=2, pady=20)
        
        self.day_vars = []
        days_frame = tk.Frame(form, bg="#FBF5E5")
        days_frame.grid(row=5, column=0, columnspan=2)
        
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.day_vars.append(var)
            
            cb_frame = tk.Frame(days_frame, bg="#FBF5E5")
            cb_frame.grid(row=0, column=i, padx=12)
            
            cb = tk.Checkbutton(cb_frame, variable=var, bg="#FBF5E5", activebackground="#FBF5E5", 
                            selectcolor="#E3FA72", highlightthickness=0)
            cb.pack(side="left")
            
            tk.Label(cb_frame, text=day, font=("Times New Roman", 10), fg="#212121", bg="#FBF5E5").pack(side="left", padx=5)

        # Button text changes based on edit mode
        button_text = "Update Habit" if self.editing_index is not None else "Add Habit"
        tk.Button(self.content, text=button_text, bg="#C89047", fg="white", width=20, height=2, 
                font=("Times New Roman", 11, "bold"), activebackground="#212121", 
                command=self.save_habit).pack(pady=40)
        
        # If editing, pre-fill the form
        if self.editing_index is not None:
            self.load_habit_for_editing()

    def load_habit_for_editing(self):
        """Load habit data into the form for editing"""
        if self.editing_index is None or self.editing_index >= len(self.habits):
            return
            
        habit = self.habits[self.editing_index]
        
        # Set category
        self.cat_var.set(habit["category"])
        
        # Update menu button text with colored dot
        menu_widgets = self.content.winfo_children()
        for widget in menu_widgets:
            if isinstance(widget, tk.Frame):  # Find the form frame
                for child in widget.winfo_children():
                    if isinstance(child, tk.Menubutton):
                        color = self.category_colors.get(habit["category"], "#777")
                        child.config(text=f"  ●  {habit['category']}")
                        break
        
        # Set task name
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, habit["name"])
        
        # Set description
        self.desc_text.delete("1.0", tk.END)
        if habit.get("description"):
            self.desc_text.insert("1.0", habit["description"])
            self.desc_text.config(fg="#212121")
        else:
            self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
            self.desc_text.config(fg="#888")
        
        # Set day checkboxes
        for i, var in enumerate(self.day_vars):
            var.set(i in habit.get("repeat_days", []))

    def save_habit(self):
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

        habit_data = {
            "name": name,
            "category": self.cat_var.get(),
            "description": description,
            "repeat_days": days
        }
        
        if self.editing_index is not None:
            # Update existing habit
            self.habits[self.editing_index] = habit_data
            messagebox.showinfo("Success!", f"Updated: {self.cat_var.get()} - {name}")
        else:
            # Add new habit
            self.habits.append(habit_data)
            messagebox.showinfo("Success!", f"Added: {self.cat_var.get()} - {name}")
        
        # Clear the form fields
        self.name_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", "Optional: Add details, notes, or motivation...")
        self.desc_text.config(fg="#888")
        
        # Uncheck all day checkboxes
        for var in self.day_vars:
            var.set(False)
        
        # Reset category selector
        cats = list(self.category_colors.keys())
        self.cat_var.set(cats[0])
        
        # Update menu button text
        menu_widgets = self.content.winfo_children()
        for widget in menu_widgets:
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Menubutton):
                        child.config(text=f"  ●  {cats[0]}")
                        break
        
        # Reset editing mode
        self.editing_index = None
        
        # Show the calendar after saving
        self.show_calendar()

    def show_view_habits(self):
        self.clear_content()
        tk.Label(self.content, text="Your Habits", font=("Times New Roman", 22, "bold"), 
                fg="#212121", bg="#FBF5E5").pack(pady=30)
        
        if not self.habits:
            tk.Label(self.content, text="No habits added yet!", 
                    font=("Times New Roman", 14), fg="#C89047", bg="#FBF5E5").pack(pady=50)
            return
        
        # Create a scrollable frame for habits
        canvas = tk.Canvas(self.content, bg="#FBF5E5", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FBF5E5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
            
        for idx, h in enumerate(self.habits):
            main_frame = tk.Frame(scrollable_frame, bg="#F0E8D8", relief="solid", bd=1)
            main_frame.pack(fill="x", padx=20, pady=8)
            
            # Top row with habit info
            top_frame = tk.Frame(main_frame, bg="#F0E8D8")
            top_frame.pack(fill="x", padx=15, pady=(10, 5))
            
            color = self.category_colors.get(h["category"], "#666")
            tk.Label(top_frame, text="●", fg=color, font=("Times New Roman", 16), bg="#F0E8D8").pack(side="left")
            
            tk.Label(top_frame, text=f"{h['category']}: {h['name']}", 
                    font=("Times New Roman", 13, "bold"), fg="#212121", bg="#F0E8D8").pack(side="left", padx=5, fill="x", expand=True)
            
            # Days display
            days = "".join(["MTWTFSS"[d] for d in h["repeat_days"]])
            tk.Label(top_frame, text=days, fg="#A35C7A", font=("Times New Roman", 11), bg="#F0E8D8").pack(side="left", padx=10)
            
            # Edit and Delete buttons
            button_frame = tk.Frame(top_frame, bg="#F0E8D8")
            button_frame.pack(side="right")
            
            # Edit button
            edit_btn = tk.Button(button_frame, text="✏️ Edit", font=("Times New Roman", 9), 
                            bg="#4CAF50", fg="white", width=8, height=1,
                            command=lambda idx=idx: self.edit_habit(idx))
            edit_btn.pack(side="left", padx=2)
            
            # Delete button
            delete_btn = tk.Button(button_frame, text="🗑️ Delete", font=("Times New Roman", 9), 
                                bg="#F44336", fg="white", width=8, height=1,
                                command=lambda idx=idx: self.delete_habit(idx))
            delete_btn.pack(side="left", padx=2)
            
            # Description row (if exists)
            if h.get("description"):
                desc_frame = tk.Frame(main_frame, bg="#F0E8D8")
                desc_frame.pack(fill="x", padx=15, pady=(0, 10))
                
                tk.Label(desc_frame, text="📝", font=("Times New Roman", 10), bg="#F0E8D8").pack(side="left")
                tk.Label(desc_frame, text=h["description"], font=("Times New Roman", 10), 
                        fg="#666", bg="#F0E8D8", wraplength=700, justify="left").pack(side="left", padx=5)

    def edit_habit(self, index):
        """Switch to edit mode for the selected habit"""
        self.editing_index = index
        self.show_add_habit()  # This will now load the habit data

    def delete_habit(self, index):
        """Delete the selected habit after confirmation"""
        if 0 <= index < len(self.habits):
            habit_name = self.habits[index]["name"]
            if messagebox.askyesno("Delete Habit", 
                                f"Are you sure you want to delete '{habit_name}'?\n\nThis will also remove all completion records for this habit."):
                
                # Remove all completion records for this habit
                for day_str in list(self.completed.keys()):
                    if index in self.completed[day_str]:
                        self.completed[day_str].remove(index)
                    # Remove empty days
                    if not self.completed[day_str]:
                        del self.completed[day_str]
                
                # Adjust indices for other habits in completed records
                for day_str in self.completed:
                    # Shift indices down for habits after the deleted one
                    self.completed[day_str] = [
                        i-1 if i > index else i 
                        for i in self.completed[day_str]
                        if i != index
                    ]
                
                # Delete the habit
                del self.habits[index]
                
                messagebox.showinfo("Success!", f"Deleted habit: {habit_name}")
                self.show_view_habits()  # Refresh the view

    def open_mood_picker(self):
        popup = tk.Toplevel(self.dash)
        popup.geometry("350x450")
        popup.title("Mood")
        popup.configure(bg="#FBF5E5")
        
        tk.Label(popup, text="How are you today?", font=("Times New Roman", 16), 
                fg="#212121", bg="#FBF5E5").pack(pady=30)

        moods = [("😊 Happy","Happy"), ("😢 Sad","Sad"), ("🎉 Excited","Excited"), 
                ("😌 Calm","Calm"), ("😴 Tired","Tired"), ("😠 Angry","Angry")]
        
        for emoji, mood in moods:
            btn = tk.Button(popup, text=emoji, font=("Times New Roman", 16), bg="#A35C7A", fg="white", 
                        width=8, height=1, activebackground="#212121",
                        command=lambda m=mood: self.set_mood(m, popup))
            btn.pack(pady=6)

    def set_mood(self, mood, popup):
        popup.destroy()
        self.mood_label.config(text=f"Today's Mood: {mood}", fg="#212121")

    def clear_content(self):
        for w in self.content.winfo_children():
            if w != self.mood_label:
                w.destroy()

    def logout(self):
        if messagebox.askyesno("Logout", "Leave HabitMate?"):
            self.dash.destroy()
            self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitMateApp(root)
    root.mainloop()