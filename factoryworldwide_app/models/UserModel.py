from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from factoryworldwide_app.server import db, login_manager
from factoryworldwide_app.models.BaseModel import Base


class User(UserMixin, Base):

    __tablename__ = "user"
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    location = db.Column(db.String(80), nullable=True)
    bio = db.Column(db.String(80), nullable=True)
    site = db.Column(db.String(80), nullable=True)
    facebook_handle = db.Column(db.String(80), nullable=True)
    twitter_handle = db.Column(db.String(80), nullable=True)
    github_handle = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
