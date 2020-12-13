from factoryworldwide_app.server import db
from factoryworldwide_app.models.BaseModel import Base


class Recipe(Base):
    __tablename__ = "recipe"
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    recipe_text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ingredients = db.relationship('Ingredient', secondary="recipe_ingredient", lazy="joined")

    def __init__(self, name=None, recipe_text=None, user_id=None):
        self.name = name
        self.recipe_text = recipe_text
        self.user_id = user_id
