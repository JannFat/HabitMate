# ================================================================
#                        HABIT SYSTEM
#  All CRUD operations for Habits, Logs, and Mood Entries
# ================================================================

import pyodbc
from datetime import datetime
from models import Habit, HabitLog, MoodEntry, User
from database import get_connection


# ================================================================
#                      USER FUNCTIONS
# ================================================================

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, password))
    conn.commit()
    conn.close()
    return True


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, username FROM users WHERE username=? AND password=?", 
                   (username, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return User(row[0], row[1])
    return None


# ================================================================
#                      HABIT FUNCTIONS
# ================================================================

def add_habit(user_id, title, description, frequency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits (user_id, title, description, frequency) 
        VALUES (?, ?, ?, ?)
    """, (user_id, title, description, frequency))

    conn.commit()
    conn.close()


def view_habits(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_id, user_id, title, created_at 
        FROM habits 
        WHERE user_id = ?
    """, (user_id,))

    habits = []
    for row in cursor.fetchall():
        habits.append(Habit(row[0], row[1], row[2], row[3]))

    conn.close()
    return habits


def update_habit(habit_id, new_title, new_description, new_frequency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habits
        SET title = ?, description = ?, frequency = ?
        WHERE habit_id = ?
    """, (new_title, new_description, new_frequency, habit_id))

    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
    conn.commit()
    conn.close()


# ================================================================
#                   HABIT LOG FUNCTIONS
# ================================================================

def add_habit_log(user_id, habit_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habit_logs (habit_id, user_id, status, log_date)
        VALUES (?, ?, ?, ?)
    """, (habit_id, user_id, status, datetime.now().date()))

    conn.commit()
    conn.close()


def view_habit_logs(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT log_id, habit_id, log_date, status
        FROM habit_logs
        WHERE user_id = ?
        ORDER BY log_date DESC
    """, (user_id,))

    logs = []
    for row in cursor.fetchall():
        logs.append(HabitLog(row[0], row[1], row[2], row[3]))

    conn.close()
    return logs


# ================================================================
#                   MOOD ENTRY FUNCTIONS
# ================================================================

def log_mood(user_id, mood_label, energy_level, positivity_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mood_entries (user_id, mood_label, energy_level, positivity_level)
        VALUES (?, ?, ?, ?)
    """, (user_id, mood_label, energy_level, positivity_level))

    conn.commit()
    conn.close()


def view_mood_entries(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mood_id, user_id, mood_label, energy_level, positivity_level, date_logged
        FROM mood_entries
        WHERE user_id = ?
        ORDER BY date_logged DESC
    """, (user_id,))

    mood_list = []
    for row in cursor.fetchall():
        mood_list.append(MoodEntry(row[0], row[1], row[2], row[3], row[4], row[5]))

    conn.close()
    return mood_list
