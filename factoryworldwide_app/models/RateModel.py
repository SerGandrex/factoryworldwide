from sqlalchemy import UniqueConstraint

from factoryworldwide_app.server import db
from factoryworldwide_app.models.BaseModel import Base


class Rate(Base):
    __tablename__ = "rate"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    rating = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user = db.relationship('User')
    recipe = db.relationship('Recipe')

    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id"),)

    def __init__(self, user_id, recipe_id=None, rating=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.rating = rating
