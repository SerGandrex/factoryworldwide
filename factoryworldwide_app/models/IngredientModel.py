from factoryworldwide_app.models.BaseModel import Base
from factoryworldwide_app.server import db


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    recipes = db.relationship("Recipe", secondary="recipe_ingredient")

    def __init__(self, name=None):
        self.name = name
