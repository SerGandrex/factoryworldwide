from sqlalchemy import func, desc

from factoryworldwide_app.models.IngredientModel import Ingredient
from factoryworldwide_app.models.RecipeModel import Recipe
from factoryworldwide_app.server import db


class IngredientService:
    model = Ingredient

    @classmethod
    def create_ingredient(cls, data):
        ingredient = cls.model(name=data['name']).save()
        return ingredient

    @classmethod
    def get_ingredient_by_id(cls, ingredient_id):
        ingredient = cls.model.get(ingredient_id)
        return ingredient

    @classmethod
    def get_most_used_ingredients(cls):
        ingredients = db.session.query(cls.model.id, cls.model.name, func.count(Recipe.id).label('ingredient_usage'))\
            .join(cls.model.recipes)\
            .group_by(cls.model.id) \
            .order_by(desc(func.count(Recipe.id))) \
            .limit(5)\
            .all()

        return ingredients
