import unittest
from unittest.mock import Mock

from factoryworldwide_app.services.RecipeIngredientService import RecipeIngredientService


class RecipeIngredientServiceTestCase(unittest.TestCase):

    def test_create_recipe_ingredient(self):
        RecipeIngredientService.model = Mock()
        RecipeIngredientService.model.return_value.save.return_value = 'recipe_ingredient'
        actual = RecipeIngredientService.create_recipe_ingredient()
        self.assertEqual('recipe_ingredient', actual)
