import unittest

from app.config.security import get_password_hash, verify_password


class SecurityTests(unittest.TestCase):
    def test_hash_and_verify_password(self):
        senha = "123456"

        hashed = get_password_hash(senha)

        self.assertIsInstance(hashed, str)
        self.assertTrue(hashed)
        self.assertTrue(verify_password(senha, hashed))
        self.assertFalse(verify_password("senha_errada", hashed))


if __name__ == "__main__":
    unittest.main()
