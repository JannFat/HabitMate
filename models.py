# ================================================
#                 MODELS.PY
#  OOP classes for Users, Habits, Habit Logs, Mood
# ================================================

from datetime import datetime


from database import get_connection

class Habit:
    def __init__(self, habit_id, user_id, title, description, frequency, created_at):
        self.habit_id = habit_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.frequency = frequency
        self.created_at = created_at

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


class HabitLog:
    def __init__(self, log_id, habit_id, user_id, log_date, status):
        self.log_id = log_id
        self.habit_id = habit_id
        self.user_id = user_id
        self.log_date = log_date
        self.status = status


class MoodEntry:
    """
    Stores user's daily mood according to Mood Meter grid.
    """

    def __init__(self, mood_id, user_id, mood_label, energy_level, positivity_level, date_logged=None):
        self.mood_id = mood_id
        self.user_id = user_id
        self.mood_label = mood_label      # e.g., "Excited", "Anxious", "Tired"
        self.energy_level = energy_level  # HIGH / LOW
        self.positivity_level = positivity_level  # POSITIVE / NEGATIVE
        self.date_logged = date_logged if date_logged else datetime.now().date()
