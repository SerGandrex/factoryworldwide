from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import render_template, Blueprint, flash, request, redirect, url_for, session
from factoryworldwide_app.forms.Forms import CreateRecipeForm, CreateIngredientForm, \
    SearchRecipeForm
from factoryworldwide_app.services.RateService import RateService
from factoryworldwide_app.services.RecipeService import RecipeService
from factoryworldwide_app.services.UserService import UserService
from factoryworldwide_app.services.IngredientService import IngredientService
from factoryworldwide_app.server import app

web = Blueprint('web', __name__, template_folder='../templates')
jwt = JWTManager(app)


@web.route('/')
def home():
    return render_template('home/index.html', title='Home')


@web.route('/create-recipe',  methods=['GET', 'POST'])
@jwt_required
def create_recipe():
    try:
        form = CreateRecipeForm()
        if form.validate_on_submit():
            data = request.form.to_dict()
            user = UserService.get_user_by_email(get_jwt_identity())
            data['ingredients'] = request.form.getlist('ingredients')
            data['user_id'] = user.id

            RecipeService.create_recipe(data)
            flash('Recipe created successfully.')
            return redirect(url_for('web.create_recipe'))

        return render_template('recipe/create-recipe.html', form=form, title='Recipe')
    except Exception:
        return render_template('error/error-page.html', title='Error')



@web.route('/get-recipe',)
@web.route('/get-recipe/<recipe_id>',)
@jwt_required
def get_recipe(recipe_id=None):
    try:
        user = UserService.get_user_by_email(get_jwt_identity())
        if recipe_id:
            recipe = RecipeService.get_recipe_by_id(recipe_id)
            return render_template('recipe/recipe.html', recipe=recipe, title='Recipe')

        recipes = RecipeService.get_recipes_with_ingredients()

        # return render_template('recipe/recipes.html', recipes=recipes['recipes'], user=user, title='Recipes')
        return render_template('recipe/recipes.html', recipes=recipes, user=user, title='Recipes')
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/get-recipe-filter/<indicator>',)
@jwt_required
def get_recipe_filter(indicator=None):
    try:
        user = UserService.get_user_by_email(get_jwt_identity())
        if indicator in ['min', 'max']:
            recipes = RecipeService.get_recipes_min_max_ingredients(indicator)
            return render_template('recipe/recipes.html', recipes=recipes, user=user, ingredient_count=True,
                                   indicator=indicator, title='Filter Recipes')

        return {'message': 'indicator not sent'}
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/get-user-recipe',)
@jwt_required
def get_user_recipe():
    try:
        user = UserService.get_user_by_email(get_jwt_identity())
        recipes = RecipeService.get_user_recipes(user.id)

        return render_template('recipe/recipes.html', recipes=recipes, user=user, title='User Recipes')
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/create-ingredient',  methods=['GET', 'POST'])
@jwt_required
def create_ingredient():
    try:
        form = CreateIngredientForm()
        if form.validate_on_submit():
            data = request.form.to_dict()
            IngredientService.create_ingredient(data)
            flash('Ingredient created successfully.')
            return redirect(url_for('web.create_ingredient'))

        return render_template('ingredient/create-ingredient.html', form=form, title='Ingredient')
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/get-ingredients')
@jwt_required
def get_ingredients():
    try:
        ingredients = IngredientService.get_most_used_ingredients()

        return render_template('ingredient/ingredients.html', ingredients=ingredients,
                               title='Ingredient')
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/rate-recipe', methods=['POST'])
@jwt_required
def rate_recipe():
    try:
        data = request.json
        data['email'] = get_jwt_identity()
        if data.get('rating').isdigit() and int(data.get('rating')) in range(1, 6):
            RateService.rate_recipe(data)
            flash('Successfully rated recipe.')
            return {'status': '200'}

        flash('Rate not valid.')
        return {'status': '400'}
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/search-recipe', methods=['GET', 'POST'])
@jwt_required
def search_recipes():
    try:
        form = SearchRecipeForm()
        if form.validate_on_submit():
            data = request.form.to_dict()
            data['ingredients'] = request.form.getlist('ingredients')
            recipes = RecipeService.search_recipes_ingredients(data)
            return render_template('recipe/recipes.html', recipes=recipes, title='User Recipes')

        return render_template('recipe/search-recipes.html', form=form, title='Search recipes')
    except Exception:
        return render_template('error/error-page.html', title='Error')


@web.route('/get-user-profile',)
@jwt_required
def get_user_profile():
    try:
        user = UserService.get_user_with_additional_info(get_jwt_identity())

        return render_template('user/user-profile.html', user=user, title='User profile')
    except Exception:
        return render_template('error/error-page.html', title='Error')
