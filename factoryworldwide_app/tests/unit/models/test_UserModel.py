import unittest
from unittest.mock import patch, Mock

from factoryworldwide_app.models.UserModel import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User()

    @patch('factoryworldwide_app.models.UserModel.check_password_hash', Mock(return_value=True))
    def test_verify_password_True(self):
        self.assertTrue(self.user.verify_password('so_secret_password'))

    @patch('factoryworldwide_app.models.UserModel.check_password_hash', Mock(return_value=False))
    def test_verify_password_False(self):
        self.assertFalse(self.user.verify_password('so_secret_password'))
