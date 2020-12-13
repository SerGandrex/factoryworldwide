import unittest
from unittest.mock import Mock, patch

from factoryworldwide_app.services.IngredientService import IngredientService


class IngredientServiceTestCase(unittest.TestCase):

    def test_get_ingredient_by_id(self):
        IngredientService.model.get = Mock(return_value='Ingredient')
        self.assertEqual(IngredientService.get_ingredient_by_id('1'), 'Ingredient')

    def test_create_ingredient(self):
        IngredientService.model.save = Mock(return_value='Ingredient')
        self.assertEqual(IngredientService.create_ingredient({'name': 'name'}), 'Ingredient')

    @patch('factoryworldwide_app.services.IngredientService.db.session.query')
    @patch('factoryworldwide_app.services.IngredientService.func.count')
    @patch('factoryworldwide_app.services.IngredientService.desc', Mock())
    def test_get_most_used_ingredients(self, count_mock, query_mock):
        count_mock.return_value = Mock()
        count_mock.return_value.label.return_value = 'label'

        query_mock.return_value.outerjoin.return_value.group_by.return_value.order_by.return_value.limit.return_value\
            .all.return_value = ['Ingredient']
        self.assertEqual(IngredientService.get_most_used_ingredients(), ['Ingredient'])

