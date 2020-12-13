from factoryworldwide_app.models.RecipeIngredientModel import RecipeIngredient


class RecipeIngredientService:
    model = RecipeIngredient

    @classmethod
    def create_recipe_ingredient(cls, **data):
        recipe_ingredient = cls.model(**data).save()
        return recipe_ingredient
