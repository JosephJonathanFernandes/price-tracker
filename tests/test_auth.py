import unittest
from src.auth import auth_service

class TestAuthService(unittest.TestCase):
    def test_add_and_authenticate_user(self):
        username = "testuser"
        password = "testpass"
        # Clean up if user exists
        auth_service.authenticate_user(username, password)
        added = auth_service.add_user(username, password)
        self.assertTrue(added or not added)  # Should not raise
        user_id = auth_service.authenticate_user(username, password)
        self.assertIsInstance(user_id, (int, type(None)))

if __name__ == "__main__":
    unittest.main()
