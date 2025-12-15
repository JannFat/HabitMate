#HabitMate


#  *HabitMate – Habit Tracking Desktop Application*

A Python-based productivity and habit-tracking desktop application built using *Tkinter*, following OOP principles, exception handling, database integration, unit testing, and modular refactoring.

HabitMate helps users build strong routines, track progress, view insights on a calendar, and record mood — all in a clean and interactive interface.

---

#  *Table of Contents*

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [System Architecture](#system-architecture)
5. [Folder Structure](#folder-structure)
6. [How to Run](#how-to-run)
7. [Screens & Workflows](#screens--workflows)
8. [Database Schema](#database-schema)
9. [Exception Handling](#exception-handling)
10. [Unit Testing](#unit-testing)
11. [Refactoring Summary](#refactoring-summary)
12. [Contributions / Roles](#contributions--roles)

---

#  *Project Overview*

HabitMate is a *desktop habit-tracking application* that allows users to create, monitor, and improve their daily routines through interactive components like:

* Dashboard
* Calendar with daily highlights
* Habit management
* Mood tracking
* Streak calculations
* Visualization of daily completion logs

The goal is to provide users with a *simple, effective, and visually pleasing* way to stay consistent.

---

#  *Features*

###  Habit Management

✔ Add habits
✔ Edit habits
✔ Delete habits
✔ Select repeat days
✔ Categorize habits
✔ Track completion
✔ View all habits in a scrollable list

###  Calendar View

✔ Highlights days based on habit completion
✔ Shows habit indicators
✔ Opens daily popup with status toggles

###  Mood Tracking

✔ Select mood from emoji picker
✔ Stores mood in database
✔ Displays on dashboard

###  Dashboard

✔ Total habits
✔ Completion summary
✔ Streak visualizer

###  Database Integration

✔ Stores habits
✔ Stores logs
✔ Stores moods
✔ Stores user data

---

#  *Tech Stack*

| Component            | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python 3.x                     |
| GUI Framework        | Tkinter                        |
| Database             | SQLite                         |
| Architecture         | OOP + Modular Design           |
| Testing Framework    | unittest                       |
| Libraries            | datetime, calendar, messagebox |

---

#  *System Architecture*

HabitMate follows a 4-layer architecture:


GUI Layer (Tkinter)
        ↓
Backend Logic (habit_system.py)
        ↓
Database Layer (SQL abstraction)
        ↓
Testing Layer (unittest)


Each layer is separate to make the system *maintainable, testable, and extensible*.

---

#  *Folder Structure*


HabitMate/
│
├── gui.py                   # Main Tkinter interface (HabitMateApp)
├── habit_system.py          # Backend business logic
├── database.py              # SQLite database abstraction
│
├── tests/
│    ├── test_users.py
│    ├── test_habits.py
│    ├── test_logs.py
│    ├── test_moods.py
│
├── assets/                  # Icons, images, logos (optional)
│
├── README.md                # This file
└── requirements.txt         # (optional)


---

#  *How to Run*

### *1. Install Python*

Make sure Python 3.x is installed.

### *2. Install dependencies*


pip install tk


### *3. Run the application*


python gui.py


---

#  *Screens & Workflows*

### *1. Dashboard*

Displays key summary metrics:

* Total habits
* Today’s completed habits
* Streak count

### *2. Calendar*

Shows:

* Completed days (green)
* Current day (yellow)
* Category-colored habit dots

### *3. Add/Edit Habit*

Includes:

* Name
* Description
* Category
* Repeat days
* Validation checks

### *4. View Habits*

A scrollable list with edit/delete buttons.

### *5. Mood Picker*

Popup with emojis for mood logging.

---

#  *Database Schema*

### *habits Table*

| Column      | Type    |
| ----------- | ------- |
| id          | INTEGER |
| name        | TEXT    |
| category    | TEXT    |
| description | TEXT    |
| repeat_days | TEXT    |
| created_on  | TEXT    |

### *habit_logs Table*

| book_id | member_id | issue_date | return_date |

### *mood Table*

| id | INTEGER |
| date | TEXT |
| mood | TEXT |

---

#  *Exception Handling*

Exception handling is applied at *three levels*:

## *1. GUI Layer*

Handled using:

python
try:
    # critical action
except Exception as e:
    messagebox.showerror("Error", str(e))


Used for:

* Saving habits
* Editing/deleting habits
* Calendar loading
* Mood saving

## *2. Backend Layer*

Database operations use:

python
try:
    cursor.execute(...)
except sqlite3.Error:
    return False


Benefits:

* Prevents crashes
* Ensures user-friendly feedback
* Improves debugging

## *3. Testing Layer*

No try-except (intentional):

* Tests must fail on errors
* Ensures backend behaves correctly

---

#  *Unit Testing*

Unit tests verify all core logic:

### *1. TestUsers*

✔ User creation
✔ Login validation

### *2. TestHabits*

✔ Add habit
✔ Update habit
✔ Delete habit

### *3. TestHabitLogs*

✔ Log habit completion
✔ Remove log

### *4. TestMoods*

✔ Add mood
✔ Fetch moods

All tests passed successfully.

---

#  *Refactoring Summary*

Refactoring included:

###  Moving logic out of GUI

GUI functions now call backend methods instead of doing work directly.

###  Improving modularity

Separated into:

* gui.py
* habit_system.py
* database.py

###  Code cleanup

* Removed repetitive blocks
* Extracted reusable functions
* Optimized UI render logic

###  Better naming and structure

Clearer methods for readability and maintainability.

---

#  *Your Role & Contributions*

In this project, I implemented:

### ✔ Full GUI Flow

Dashboard, Calendar, Habit CRUD, Mood Picker, Daily View.

### ✔ Backend Logic

Habit management, log tracking, mood system.

### ✔ Database Integration

Abstraction layer + CRUD operations.

### ✔ Exception Handling

Implemented across GUI + backend.

### ✔ Unit Testing

Wrote separate test cases for each module.

### ✔ Refactoring

Improved structure, readability, modularity, and error handling.

### ✔ Documentation

Created complete:

* Project report
* UML diagrams
* README.md
* Architecture explanation



#  *Thank You for Using HabitMate!*
