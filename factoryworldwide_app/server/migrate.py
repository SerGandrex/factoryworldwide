from flask_migrate import Migrate
from factoryworldwide_app.server import app, db
from factoryworldwide_app.models import UserModel, RecipeModel, IngredientModel, RateModel, RecipeIngredientModel

migrate = Migrate(app, db)
