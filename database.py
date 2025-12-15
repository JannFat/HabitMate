# database.py
# Robust DB helper: each function opens/closes its own connection.
from datetime import date
import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=DESKTOP-FPQ15DO;"   # update if your server name differs
            "DATABASE=HabitMate3;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
        )
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None

# -------------------------
# USER FUNCTIONS
# -------------------------
def register_user(username, password):
    """
    Returns (success: bool, message: str)
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            return False, "❌ Username already exists"

        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "✅ Account created successfully"
    except Exception as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()

def login_user(username, password):
    """
    Returns (success: bool, user_id_or_None)
    """
    conn = get_connection()
    if not conn:
        return False, None

    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        row = cur.fetchone()
        if row:
            return True, row[0]
        return False, None
    except Exception as e:
        print("Login DB error:", e)
        return False, None
    finally:
        conn.close()

# -------------------------
# HABIT FUNCTIONS (simple)
# -------------------------
def add_habit(user_id, title, description, frequency):
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO habits (user_id, title, description, frequency, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, title, description, frequency, date.today())
        )
        conn.commit()
    finally:
        conn.close()

def get_habits(user_id):
    """
    Returns list of rows from habits table for the user.
    Each row will be a tuple as returned by pyodbc.
    Caller should transform rows to dicts if needed.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT habit_id, title, description, frequency, created_at FROM habits WHERE user_id = ?", (user_id,))
        return cur.fetchall()
    finally:
        conn.close()

def delete_habit(habit_id):
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM habit_logs WHERE habit_id = ?", (habit_id,))
        cur.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
        conn.commit()
    finally:
        conn.close()

# -------------------------
# MOOD (optional)
# -------------------------
def add_mood_entry(user_id, mood_label, energy, positivity):
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO mood_entries (user_id, mood_label, energy_level, positivity_level, date_logged) VALUES (?, ?, ?, ?, ?)",
            (user_id, mood_label, energy, positivity, date.today())
        )
        conn.commit()
    finally:
        conn.close()

def add_habit_log(user_id, habit_id, status):
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO habit_logs (user_id, habit_id, status, log_date)
            VALUES (?, ?, ?, CAST(GETDATE() AS DATE))
        """, (user_id, habit_id, status))
        conn.commit()
        return True
    except Exception as e:
        print("Error inserting habit log:", e)
        return False
    finally:
        conn.close()


def get_habit_logs(user_id):
    """
    Returns list of (habit_id, log_date)
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT habit_id, log_date 
            FROM habit_logs 
            WHERE user_id = ?
            ORDER BY log_date
        """, (user_id,))
        return cur.fetchall()
    except:
        return []
    finally:
        conn.close()
