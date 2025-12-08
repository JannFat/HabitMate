import sys
import os

# Add parent directory so Python can find habit_system.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from habit_system import add_mood_entry, get_mood_entries

class TestMoods(unittest.TestCase):

    def setUp(self):
        self.test_user_id = 1
        add_mood_entry(self.test_user_id, "Happy")

    def test_mood_entries(self):
        moods = get_mood_entries(self.test_user_id)
        self.assertTrue(any(m[1] == "Happy" for m in moods))  # m[1] = mood_label


if __name__ == "__main__":
    unittest.main()
