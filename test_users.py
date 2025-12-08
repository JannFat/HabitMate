import sys
import os

# Add parent directory so Python can find habit_system.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from habit_system import register_user, login_user, get_user_by_id

class TestUsers(unittest.TestCase):

    def setUp(self):
        # Create a test user
        self.test_username = "testuser"
        self.test_password = "123"
        register_user(self.test_username, self.test_password)
    
    def test_register_login(self):
        # Test login
        success, user_id = login_user(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertIsInstance(user_id, int)

        # Optional: fetch username
        user_obj = get_user_by_id(user_id)
        self.assertIsNotNone(user_obj)
        self.assertEqual(user_obj.username, self.test_username)


if __name__ == "__main__":
    unittest.main()

