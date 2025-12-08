import sys
import os

# Add parent directory so Python can find habit_system.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from habit_system import add_habit, add_habit_log, get_habit_logs, delete_habit

class TestHabitLogs(unittest.TestCase):

    def setUp(self):
        self.test_user_id = 1
        self.habit_id = add_habit(self.test_user_id, "Habit for Log")
        add_habit_log(self.test_user_id, self.habit_id)  # default status="completed"

    def tearDown(self):
        delete_habit(self.habit_id)

    def test_habit_logs(self):
        logs = get_habit_logs(self.test_user_id)
        self.assertTrue(any(log[0] == self.habit_id for log in logs))  # log[0] = habit_id


if __name__ == "__main__":
    unittest.main()
