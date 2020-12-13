import unittest
from dataclasses import dataclass
from typing import Any
from unittest.mock import Mock, patch, call

from factoryworldwide_app.services.UserService import UserService


@dataclass
class User:
    email: Any = None
    first_name: Any = None
    last_name: Any = None
    password: Any = None
    location: Any = None
    bio: Any = None
    site: Any = None
    facebook_handle: Any = None
    twitter_handle: Any = None
    github_handle: Any = None
    password_hash: Any = None

    def verify_password(self, password):
        return self.password == password


class UserServiceTestCase(unittest.TestCase):

    @patch('factoryworldwide_app.services.UserService.UserService._get_additional_info', Mock(return_value={}))
    def test_create_user(self):
        expected = User(email='some_email@test.com', first_name='some_first_name', last_name='some_last_name',
                        password='so_secret_password')

        UserService.model = Mock()
        actual = UserService.create_user(
            {'email': 'some_email@test.com', 'first_name': 'some_first_name', 'last_name': 'some_last_name',
             'password': 'so_secret_password'})

        self._assert_data(actual, expected, 'email', 'first_name', 'last_name', 'password')
        self._assert_never_called(actual, 'location', 'bio', 'site', 'facebook', 'twitter', 'git')
        UserService.model.assert_has_calls(calls=[call().save()])

    @patch('factoryworldwide_app.services.UserService.clearbit.Enrichment.find',
           Mock(return_value={'person': {'location': 'some_location', 'bio': 'some_bio', 'site': 'some_site',
                                         'facebook': {'handle': 'some_facebook'}, 'twitter': {'handle': 'some_twitter'},
                                         'github': {'handle': 'some_git'}}}))
    def test_create_user_additional_info(self):
        expected = User(email='some_email@test.com', first_name='some_first_name', last_name='some_last_name',
                        password='so_secret_password', location='some_location', bio='some_bio', site='some_site',
                        facebook_handle='some_facebook', twitter_handle='some_twitter', github_handle='some_git')
        UserService.model = Mock()
        actual = UserService.create_user(
            {'email': 'some_email@test.com', 'first_name': 'some_first_name', 'last_name': 'some_last_name',
             'password': 'so_secret_password', 'location': 'some_location', 'bio': 'some_bio', 'site': 'some_site',
             'facebook_handle': {'handle': 'some_facebook'}, 'twitter_handle': {'handle': 'some_twitter'},
             'github_handle': {'handle': 'some_git'}})

        self._assert_data(actual, expected, 'email', 'first_name', 'last_name', 'password', 'location', 'bio', 'site',
                          'facebook_handle', 'twitter_handle', 'github_handle')
        UserService.model.assert_has_calls(calls=[call().save()])

    def test_login(self):
        UserService.model.filter = Mock(return_value=User(email='test@test.com', password='so_secret_password'))
        actual = UserService.login({'email': 'test@test.com', 'password': 'so_secret_password'})

        self.assertEqual(vars(User(email='test@test.com', password='so_secret_password')), vars(actual))

    def test_login_failure(self):
        UserService.model.filter = Mock(return_value=None)
        actual = UserService.login({'email': 'test@test.com', 'password': 'so_secret_password'})

        self.assertEqual(None, actual)

    def test_login_verify_password_False(self):
        UserService.model.filter = Mock(return_value=User(email='test@email.com', password='this_is_not_my_password'))
        actual = UserService.login({'email': 'test@test.com', 'password': 'so_secret_password'})

        self.assertEqual(None, actual)

    def test_get_user_by_email(self):
        UserService.model.filter = Mock(return_value='User')
        self.assertEqual(UserService.get_user_by_email('test@test.com'), 'User')

    def test_get_user_with_additional_info(self):
        expected = vars(User(email='test@email.com'))
        expected.pop('password_hash')
        UserService.get_user_by_email = Mock(return_value=User(email='test@email.com'))
        user_data = UserService.get_user_with_additional_info({'email': 'test@email.com'})

        self.assertEqual(expected, user_data)

    @patch('factoryworldwide_app.services.UserService.clearbit.Enrichment.find',
           Mock(return_value={'person': {'location': 'some_location', 'bio': 'some_bio', 'site': 'some_site',
                                         'facebook': {'handle': 'some_facebook'}, 'twitter': {'handle': 'some_twitter'},
                                         'github': {'handle': 'some_git'}}}))
    def test_get_additional_info(self):
        actual = UserService._get_additional_info('test@email.com')

        self.assertEqual({'location': 'some_location', 'bio': 'some_bio', 'site': 'some_site',
                                         'facebook': {'handle': 'some_facebook'}, 'twitter': {'handle': 'some_twitter'},
                                         'github': {'handle': 'some_git'}}, actual)

    @patch('factoryworldwide_app.services.UserService.clearbit.Enrichment.find', Mock(return_value={}))
    def test_get_additional_info_None(self):
        actual = UserService._get_additional_info('test@email.com')

        self.assertEqual({}, actual)

    def _assert_data(self, actual, expected, *args):
        for arg in args:
            self.assertEqual(getattr(expected, arg), getattr(actual, arg))

    def _assert_never_called(self, actual, *args):
        for arg in args:
            arg_call = getattr(actual, arg)
            self.assertEqual(arg_call.call_count, 0)
