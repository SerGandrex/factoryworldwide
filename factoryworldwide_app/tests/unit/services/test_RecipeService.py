import unittest
from unittest.mock import Mock, patch

from factoryworldwide_app.services.RecipeService import RecipeService


class RecipeServiceTestCase(unittest.TestCase):

    @patch('factoryworldwide_app.services.RecipeService.IngredientService.get_ingredient_by_id', Mock())
    @patch('factoryworldwide_app.services.RecipeService.RecipeIngredientService.create_recipe_ingredient', Mock())
    def test_create_recipe(self):
        RecipeService.model.save = Mock(return_value='recipe')
        actual = RecipeService.create_recipe(
            {'ingredients': [1, 2], 'name': 'recipe_name', 'text': 'recipe_text', 'user_id': 1})

        self.assertEqual('recipe', actual)

    @patch('factoryworldwide_app.services.RecipeService.db.session.query')
    @patch('factoryworldwide_app.services.RecipeService.func.avg')
    def test_get_user_recipes(self, avg_mock, query_mock):
        avg_mock.return_value = Mock()
        avg_mock.return_value.label.return_value = 'label'

        query_mock.return_value.join.return_value.outerjoin.return_value.group_by.return_value.filter.return_value.\
            paginate.return_value = ['recipe_1', 'recipe_2']

        actual = RecipeService.get_user_recipes(1)

        self.assertEqual(['recipe_1', 'recipe_2'], actual)

    def test_get_recipe_by_id(self):
        RecipeService.model.get = Mock(return_value='Recipe')
        self.assertEqual(RecipeService.get_recipe_by_id('1'), 'Recipe')

    @patch('factoryworldwide_app.services.RecipeService.db.session.query')
    @patch('factoryworldwide_app.services.RecipeService.func.avg')
    def test_get_recipes_with_ingredients(self, avg_mock, query_mock):
        avg_mock.return_value = Mock()
        avg_mock.return_value.label.return_value = 'label'

        query_mock.return_value.outerjoin.return_value.group_by.return_value.paginate.return_value = [
            'recipe_1', 'recipe_2']

        actual = RecipeService.get_recipes_with_ingredients()

        self.assertEqual(['recipe_1', 'recipe_2'], actual)

    @patch('factoryworldwide_app.services.RecipeService.db.session.query')
    @patch('factoryworldwide_app.services.RecipeService.func.avg')
    @patch('factoryworldwide_app.services.RecipeService.and_', Mock())
    def test_search_recipes_ingredients(self, avg_mock, query_mock):
        RecipeService.model = Mock()
        avg_mock.return_value = Mock()
        avg_mock.return_value.label.return_value = 'label'

        query_mock.return_value.join.return_value.outerjoin.return_value.group_by.return_value.filter.return_value.\
            paginate.return_value = ['recipe_1']

        actual = RecipeService.search_recipes_ingredients({'recipe_name': 'some_recipe_name'})

        self.assertEqual(['recipe_1'], actual)

    @patch('factoryworldwide_app.services.RecipeService.db.session.query')
    @patch('factoryworldwide_app.services.RecipeService.func.avg')
    @patch('factoryworldwide_app.services.RecipeService.func.count')
    @patch('factoryworldwide_app.services.RecipeService.func.min')
    def test_get_recipes_min_max_ingredients(self, min_mock, count_mock, avg_mock, query_mock):
        RecipeService.model = Mock()
        min_mock.return_value = Mock()
        min_mock.return_value.label.return_value = 'label'

        count_mock.return_value = Mock()
        count_mock.return_value.label.return_value = 'label'

        avg_mock.return_value = Mock()
        avg_mock.return_value.label.return_value = 'label'

        query_mock.return_value.filter.return_value.outerjoin.return_value.group_by.return_value. \
            paginate.return_value = ['recipe_1']

        actual = RecipeService.get_recipes_min_max_ingredients('min')

        self.assertEqual(['recipe_1'], actual)
