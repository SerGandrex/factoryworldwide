from sqlalchemy import UniqueConstraint

from factoryworldwide_app.server import db
from factoryworldwide_app.models.BaseModel import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    recipe = db.relationship('Recipe', backref='recipe_ingredients', lazy='joined')
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients', lazy='joined')

    __table_args__ = (
        UniqueConstraint("recipe_id", "ingredient_id"),)

    def __init__(self, recipe=None, ingredient=None):
        self.recipe = recipe
        self.ingredient = ingredient
