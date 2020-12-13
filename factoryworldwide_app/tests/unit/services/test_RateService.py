import unittest
from unittest.mock import Mock, patch

from factoryworldwide_app.services.RateService import RateService


class RateServiceTestCase(unittest.TestCase):

    @patch('factoryworldwide_app.services.RateService.UserService.get_user_by_email', Mock())
    @patch('factoryworldwide_app.services.RateService.RecipeService.get_recipe_by_id', Mock())
    def test_rate_recipe_update(self):
        RateService.model.get = Mock()
        RateService.model.update = Mock()
        RateService.rate_recipe({'email': 'some_email', 'recipe_id': 'some_recipe_id', 'rating': 5})
        RateService.model.update.assert_called_once()

    @patch('factoryworldwide_app.services.RateService.UserService.get_user_by_email', Mock())
    @patch('factoryworldwide_app.services.RateService.RecipeService.get_recipe_by_id', Mock())
    def test_rate_recipe_save(self):
        RateService.model.get = Mock(return_value=None)
        RateService.model.save = Mock()
        RateService.rate_recipe({'email': 'some_email', 'recipe_id': 'some_recipe_id', 'rating': 5})
        RateService.model.save.assert_called_once()


