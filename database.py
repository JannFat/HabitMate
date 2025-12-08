# database.py
# Robust DB helper: each function opens/closes its own connection.
from datetime import date
import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=DESKTOP-FPQ15DO;"   # update if your server name differs
            "DATABASE=HabitMate2;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
        )
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None

def get_table_columns(table_name):
    """Get the actual column names from a table"""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)
        columns = [row[0] for row in cur.fetchall()]
        return columns
    except Exception as e:
        print(f"Error getting table columns: {e}")
        return []
    finally:
        conn.close()

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

        print(f"[DEBUG] Registering user - username: {username}")
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"[DEBUG] User registered successfully")
        
        # Verify it was saved
        cur.execute("SELECT user_id, username FROM users WHERE username = ?", (username,))
        verify = cur.fetchone()
        if verify:
            print(f"[DEBUG] Verification: Found user in DB - ID: {verify[0]}, Username: {verify[1]}")
        
        return True, "✅ Account created successfully"
    except Exception as e:
        print(f"[ERROR] Error in register_user: {e}")
        import traceback
        traceback.print_exc()
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
    """Add a new habit and return the habit_id"""
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        # Use actual column names: habit_name (not title), description, no frequency column
        # Store frequency in description if needed, or append it
        if frequency:
            # Append frequency info to description if description exists
            full_description = description
            if full_description:
                full_description += f" | Frequency: {frequency}"
            else:
                full_description = f"Frequency: {frequency}"
        else:
            full_description = description
        
        print(f"[DEBUG] Adding habit - user_id: {user_id}, habit_name: {title}, description: {full_description[:50]}...")
        
        cur.execute(
            "INSERT INTO habits (user_id, habit_name, description, created_at) VALUES (?, ?, ?, ?)",
            (user_id, title, full_description, date.today())
        )
        conn.commit()
        print(f"[DEBUG] Habit inserted, committing transaction...")
        
        # Get the newly inserted habit_id
        cur.execute("SELECT @@IDENTITY")
        habit_id = cur.fetchone()[0]
        print(f"[DEBUG] Habit saved successfully with habit_id: {habit_id}")
        
        # Verify it was saved
        cur.execute("SELECT habit_id, habit_name FROM habits WHERE habit_id = ?", (habit_id,))
        verify = cur.fetchone()
        if verify:
            print(f"[DEBUG] Verification: Found habit in DB - ID: {verify[0]}, Name: {verify[1]}")
        else:
            print(f"[DEBUG] WARNING: Habit not found in database after insert!")
        
        return habit_id
    except Exception as e:
        print(f"[ERROR] Error in add_habit: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

def get_habits(user_id):
    """
    Returns list of rows from habits table for the user.
    Each row will be a tuple as returned by pyodbc.
    Caller should transform rows to dicts if needed.
    Actual columns: (habit_id, habit_name, description, created_at)
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        # Use actual column names: habit_name instead of title
        cur.execute("SELECT habit_id, habit_name, description, created_at FROM habits WHERE user_id = ?", (user_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error in get_habits: {e}")
        return []
    finally:
        conn.close()

def update_habit(habit_id, title, description, frequency):
    """Update an existing habit"""
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        # Use actual column names: habit_name instead of title, no frequency column
        # Store frequency in description if needed
        if frequency:
            # Append frequency info to description if description exists
            full_description = description
            if full_description:
                full_description += f" | Frequency: {frequency}"
            else:
                full_description = f"Frequency: {frequency}"
        else:
            full_description = description
        
        cur.execute(
            "UPDATE habits SET habit_name = ?, description = ? WHERE habit_id = ?",
            (title, full_description, habit_id)
        )
        conn.commit()
    except Exception as e:
        print(f"Error in update_habit: {e}")
        raise
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
# HABIT LOG FUNCTIONS
# -------------------------
def add_habit_log(user_id, habit_id, log_date, status="completed"):
    """Add a habit completion log"""
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        # Check if log already exists for this habit and date
        cur.execute(
            "SELECT log_id FROM habit_logs WHERE habit_id = ? AND user_id = ? AND log_date = ?",
            (habit_id, user_id, log_date)
        )
        if cur.fetchone():
            # Log already exists, update it
            print(f"[DEBUG] Updating existing habit log - habit_id: {habit_id}, date: {log_date}")
            cur.execute(
                "UPDATE habit_logs SET status = ? WHERE habit_id = ? AND user_id = ? AND log_date = ?",
                (status, habit_id, user_id, log_date)
            )
        else:
            # Insert new log
            print(f"[DEBUG] Adding new habit log - habit_id: {habit_id}, user_id: {user_id}, date: {log_date}")
            cur.execute(
                "INSERT INTO habit_logs (habit_id, user_id, log_date, status) VALUES (?, ?, ?, ?)",
                (habit_id, user_id, log_date, status)
            )
        conn.commit()
        print(f"[DEBUG] Habit log saved successfully")
    except Exception as e:
        print(f"[ERROR] Error in add_habit_log: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

def delete_habit_log(user_id, habit_id, log_date):
    """Delete a habit completion log"""
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM habit_logs WHERE habit_id = ? AND user_id = ? AND log_date = ?",
            (habit_id, user_id, log_date)
        )
        conn.commit()
    finally:
        conn.close()

def get_habit_logs(user_id):
    """Get all habit logs for a user. Returns list of (habit_id, log_date) tuples"""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT habit_id, log_date FROM habit_logs WHERE user_id = ? AND status = 'completed'",
            (user_id,)
        )
        return cur.fetchall()
    finally:
        conn.close()

# -------------------------
# MOOD (optional)
# -------------------------
def add_mood_entry(user_id, mood_label):
    """Add a mood entry without energy_level and positivity_level"""
    conn = get_connection()
    if not conn:
        raise RuntimeError("DB connection failed")
    try:
        cur = conn.cursor()
        print(f"[DEBUG] Adding mood entry - user_id: {user_id}, mood: {mood_label}")
        cur.execute(
            "INSERT INTO mood_entries (user_id, mood_label, date_logged) VALUES (?, ?, ?)",
            (user_id, mood_label, date.today())
        )
        conn.commit()
        print(f"[DEBUG] Mood entry saved successfully")
    except Exception as e:
        print(f"[ERROR] Error in add_mood_entry: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

# -------------------------
# VERIFICATION FUNCTIONS
# -------------------------
def verify_all_data():
    """Print all data in database for debugging"""
    conn = get_connection()
    if not conn:
        print("[ERROR] Cannot connect to database")
        return
    
    try:
        cur = conn.cursor()
        
        print("\n" + "="*50)
        print("DATABASE VERIFICATION")
        print("="*50)
        
        # Check users
        cur.execute("SELECT user_id, username, created_at FROM users")
        users = cur.fetchall()
        print(f"\nUSERS TABLE: {len(users)} records")
        for u in users:
            print(f"  - ID: {u[0]}, Username: {u[1]}, Created: {u[2]}")
        
        # Check habits
        cur.execute("SELECT habit_id, user_id, habit_name, description, created_at FROM habits")
        habits = cur.fetchall()
        print(f"\nHABITS TABLE: {len(habits)} records")
        for h in habits:
            print(f"  - ID: {h[0]}, User ID: {h[1]}, Name: {h[2]}, Description: {h[3][:50] if h[3] else 'None'}..., Created: {h[4]}")
        
        # Check habit_logs
        cur.execute("SELECT log_id, habit_id, user_id, log_date, status FROM habit_logs")
        logs = cur.fetchall()
        print(f"\nHABIT_LOGS TABLE: {len(logs)} records")
        for l in logs:
            print(f"  - Log ID: {l[0]}, Habit ID: {l[1]}, User ID: {l[2]}, Date: {l[3]}, Status: {l[4]}")
        
        # Check mood_entries
        cur.execute("SELECT mood_id, user_id, mood_label, date_logged FROM mood_entries")
        moods = cur.fetchall()
        print(f"\nMOOD_ENTRIES TABLE: {len(moods)} records")
        for m in moods:
            print(f"  - Mood ID: {m[0]}, User ID: {m[1]}, Mood: {m[2]}, Date: {m[3]}")
        
        print("\n" + "="*50 + "\n")
        
    except Exception as e:
        print(f"[ERROR] Error verifying data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
