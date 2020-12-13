from sqlalchemy import func, and_
from factoryworldwide_app.models.RateModel import Rate
from factoryworldwide_app.models.RecipeModel import Recipe
from factoryworldwide_app.models.IngredientModel import Ingredient
from factoryworldwide_app.models.UserModel import User
from factoryworldwide_app.server import db
from factoryworldwide_app.services.RecipeIngredientService import RecipeIngredientService
from factoryworldwide_app.services.IngredientService import IngredientService
ROWS_PER_PAGE = 8


class RecipeService:
    model = Recipe

    @classmethod
    def create_recipe(cls, data):
        recipe = cls.model(name=data['name'], recipe_text=data['text'], user_id=data['user_id']).save()

        for ingredient_id in data['ingredients']:
            ingredient = IngredientService.get_ingredient_by_id(ingredient_id)
            RecipeIngredientService.create_recipe_ingredient(recipe=recipe,
                                                             ingredient=ingredient)
        return recipe

    @classmethod
    def get_user_recipes(cls, user_id):
        recipes = db.session.query(cls.model.id, cls.model.name, cls.model.recipe_text, cls.model.user_id,
                                   func.avg(Rate.rating).label("rating"))\
            .join(User, cls.model.user_id == User.id)\
            .outerjoin(Rate, cls.model.id == Rate.recipe_id)\
            .group_by(cls.model.id)\
            .filter(User.id == user_id) \
            .paginate(per_page=ROWS_PER_PAGE)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        recipe = cls.model.get(recipe_id)
        return recipe

    @classmethod
    def get_recipes_with_ingredients(cls):
        recipes = db.session.query(cls.model.id, cls.model.name, cls.model.recipe_text, cls.model.user_id,
                                   func.avg(Rate.rating).label("rating"))\
                                   .outerjoin(Rate, cls.model.id == Rate.recipe_id)\
                                   .group_by(cls.model.id)\
                                   .paginate(per_page=ROWS_PER_PAGE)

        return recipes

    @classmethod
    def search_recipes_ingredients(cls, data):
        query = db.session.query(cls.model.id, cls.model.name, cls.model.recipe_text, cls.model.user_id,
                                 func.avg(Rate.rating).label("rating"))\
            .join(cls.model.ingredients)\
            .outerjoin(Rate, cls.model.id == Rate.recipe_id)\
            .group_by(cls.model.id)\
            .filter(and_(cls.model.name.contains(data.get('recipe_name')),
                         cls.model.recipe_text.contains(data.get('recipe_text'))))\

        if data.get('ingredients'):
            query = query.filter(Ingredient.name.in_(data.get('ingredients')))

        recipes = query.paginate(per_page=ROWS_PER_PAGE)

        return recipes

    @classmethod
    def get_recipes_min_max_ingredients(cls, indicator):

        sub1 = db.session.query(cls.model.id, cls.model.name, cls.model.recipe_text, cls.model.user_id,
                                func.count(Ingredient.id).label("ingredient_count")) \
            .join(cls.model.ingredients) \
            .group_by(cls.model.id).subquery()

        if indicator == 'min':
            sub2 = db.session.query(func.min(sub1.c.ingredient_count).label('min_count'))\
                .first().min_count
        else:
            sub2 = db.session.query(func.max(sub1.c.ingredient_count).label('max_count')) \
                .first().max_count

        recipes = db.session.query(sub1.c.id, sub1.c.name, sub1.c.recipe_text, sub1.c.user_id, sub1.c.ingredient_count,
                                   func.avg(Rate.rating).label("rating"))\
            .filter(sub1.c.ingredient_count == sub2)\
            .outerjoin(Rate, sub1.c.id == Rate.recipe_id)\
            .group_by(sub1.c.id)\
            .paginate(per_page=ROWS_PER_PAGE)

        return recipes
