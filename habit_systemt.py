# ================================================================
#                        HABIT SYSTEM
#  All CRUD operations for Habits, Logs, and Mood Entries
# ================================================================

import pyodbc
from datetime import datetime
from models import Habit, HabitLog, MoodEntry, User
from datetime import date
from collections import namedtuple
from pyodbc import DatabaseError, IntegrityError, OperationalError, ProgrammingError, InterfaceError
from database import get_connection

conn, cursor = get_connection()

# ================================================================
#                      USER FUNCTIONS
# ================================================================


def get_user_by_id(user_id):
    try:
        with db_cursor() as cur:
            cur.execute("SELECT user_id, username FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            if row:
                return type("User", (), {"user_id": row[0], "username": row[1]})()
            return None
    except Exception as e:
        print(f"[ERROR] get_user_by_id: {e}")
        return None



def register_user(username, password):
    try:
        with db_cursor() as cur:
            cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
            if cur.fetchone():
                return False, "Username already exists"
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return True, "Account created"
    except Exception as e:
        print(f"[ERROR] register_user: {e}")
        return False, "DB error"


User = namedtuple("User", ["user_id", "username"])
def login_user(username, password):
    try:
        with db_cursor() as cur:
            cur.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
            row = cur.fetchone()
            if row:
                return True, row[0]
            return False, None  # login failed
    except DatabaseError as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False, None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False, None


# ================================================================
#                      HABIT FUNCTIONS
# ================================================================

Habit = namedtuple("Habit", ["habit_id"])
def add_habit(user_id, habit_name, description=None, frequency=None):
    if not user_id or not habit_name:
        print("[ERROR] Missing required fields: user_id and habit_name")
        return None

    try:
        full_description = description or ""
        if frequency:
            full_description += (
                f" | Frequency: {frequency}" if description else f"Frequency: {frequency}"
            )

        with db_cursor() as cur:
            cur.execute(
                "INSERT INTO habits (user_id, habit_name, description, created_at) "
                "VALUES (?, ?, ?, ?)",
                (user_id, habit_name, full_description, date.today())
            )

            cur.execute("SELECT @@IDENTITY")
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                print("[ERROR] Failed to retrieve habit_id after insert")
                return None

    except IntegrityError as e:
        print(f"[WARN] Integrity issue (duplicate habit/user missing): {e}")
    except OperationalError as e:
        print(f"[ERROR] Database unavailable or connection dropped: {e}")
    except ProgrammingError as e:
        print(f"[ERROR] SQL syntax/parameter error: {e}")
    except InterfaceError as e:
        print(f"[ERROR] Cursor/connection misuse: {e}")
    except (TypeError, ValueError) as e:
        print(f"[ERROR] Invalid input data type: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

    return None


def get_habits(user_id):
    """Get all habits for a user"""
    try:
        with db_cursor() as cur:
            cur.execute("SELECT habit_id, habit_name, description, created_at FROM habits WHERE user_id=?", (user_id,))
            rows = cur.fetchall()
            return rows  # list of tuples
    except Exception as e:
        print(f"[ERROR] get_habits: {e}")
        return []

def update_habit(habit_id, habit_name=None, description=None, frequency=None):
    """Update an existing habit"""
    try:
        full_description = description or ""
        if frequency:
            full_description += f" | Frequency: {frequency}" if description else f"Frequency: {frequency}"

        with db_cursor() as cur:
            cur.execute(
                "UPDATE habits SET habit_name=?, description=? WHERE habit_id=?",
                (habit_name, full_description, habit_id)
            )
            return True
    except Exception as e:
        print(f"[ERROR] update_habit: {e}")
        return False

def delete_habit(habit_id):
    """Delete a habit and its logs"""
    try:
        with db_cursor() as cur:
            # Delete related logs first
            cur.execute("DELETE FROM habit_logs WHERE habit_id=?", (habit_id,))
            cur.execute("DELETE FROM habits WHERE habit_id=?", (habit_id,))
            return True
    except Exception as e:
        print(f"[ERROR] delete_habit: {e}")
        return False

# ================================================================
#                   HABIT LOG FUNCTIONS
# ================================================================


def add_habit_log(user_id, habit_id, status="completed", log_date=None):
    """Add or update a habit log"""
    log_date = log_date or date.today()
    try:
        with db_cursor() as cur:
            # Check if log exists
            cur.execute("SELECT log_id FROM habit_logs WHERE habit_id=? AND user_id=? AND log_date=?", 
                        (habit_id, user_id, log_date))
            if cur.fetchone():
                cur.execute(
                    "UPDATE habit_logs SET status=? WHERE habit_id=? AND user_id=? AND log_date=?",
                    (status, habit_id, user_id, log_date)
                )
            else:
                cur.execute(
                    "INSERT INTO habit_logs (habit_id, user_id, log_date, status) VALUES (?, ?, ?, ?)",
                    (habit_id, user_id, log_date, status)
                )
            return True
    except Exception as e:
        print(f"[ERROR] add_habit_log: {e}")
        return False

def get_habit_logs(user_id):
    """Get all habit logs for a user"""
    try:
        with db_cursor() as cur:
            cur.execute("SELECT habit_id, log_date, status FROM habit_logs WHERE user_id=? AND status='completed'", (user_id,))
            return cur.fetchall()
    except Exception as e:
        print(f"[ERROR] get_habit_logs: {e}")
        return []

def delete_habit_log(user_id, habit_id, log_date):
    """Delete a habit log"""
    try:
        with db_cursor() as cur:
            cur.execute("DELETE FROM habit_logs WHERE habit_id=? AND user_id=? AND log_date=?", (habit_id, user_id, log_date))
            return True
    except Exception as e:
        print(f"[ERROR] delete_habit_log: {e}")
        return False
# ================================================================
#                   MOOD ENTRY FUNCTIONS
# ================================================================

def add_mood_entry(user_id, mood_label):
    """Add a mood entry"""
    try:
        with db_cursor() as cur:
            cur.execute(
                "INSERT INTO mood_entries (user_id, mood_label, date_logged) VALUES (?, ?, ?)",
                (user_id, mood_label, date.today())
            )
            return True
    except Exception as e:
        print(f"[ERROR] add_mood_entry: {e}")
        return False

def get_mood_entries(user_id):
    """Get all mood entries"""
    try:
        with db_cursor() as cur:
            cur.execute(
                "SELECT mood_id, mood_label, date_logged FROM mood_entries WHERE user_id=? ORDER BY date_logged DESC",
                (user_id,)
            )
            return cur.fetchall()
    except Exception as e:
        print(f"[ERROR] get_mood_entries: {e}")
        return []
