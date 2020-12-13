from factoryworldwide_app.models.RateModel import Rate
from factoryworldwide_app.services.UserService import UserService
from factoryworldwide_app.services.RecipeService import RecipeService


class RateService:
    model = Rate

    @classmethod
    def rate_recipe(cls, data):
        user = UserService.get_user_by_email(data['email'])
        recipe = RecipeService.get_recipe_by_id(data['recipe_id'])
        if recipe.user_id != user.id:
            rate = cls.model.get((user.id, data['recipe_id']))
            if rate:
                rate.rating = data['rating']
                cls.model.update(rate)
            else:
                cls.model(recipe_id=data['recipe_id'], user_id=user.id, rating=data['rating']).save()
