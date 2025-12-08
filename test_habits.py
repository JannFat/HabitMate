import sys
import os

# Add parent directory so Python can find habit_system.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from habit_system import add_habit, get_habits, update_habit, delete_habit

class TestHabits(unittest.TestCase):

    def setUp(self):
        self.test_user_id = 1
        self.habit_id = add_habit(self.test_user_id, "Test Habit", "Description", "Daily")

    def tearDown(self):
        delete_habit(self.habit_id)

    def test_habit_crud(self):
        # Read
        habits = get_habits(self.test_user_id)
        self.assertTrue(any(h[0] == self.habit_id for h in habits))  # h[0] = habit_id

        # Update
        updated = update_habit(self.habit_id, "Updated Habit", "Updated Desc", "Weekly")
        self.assertTrue(updated)

        # Verify update
        habits = get_habits(self.test_user_id)
        self.assertTrue(any(h[0] == self.habit_id and h[1] == "Updated Habit" for h in habits))


if __name__ == "__main__":
    unittest.main()

