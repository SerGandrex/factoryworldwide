from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

from factoryworldwide_app.models.UserModel import User
from factoryworldwide_app.models.IngredientModel import Ingredient
from factoryworldwide_app.server import hunter


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
        email_verifier = hunter.email_verifier(field.data)
        if not email_verifier or email_verifier['result'] == 'undeliverable':
            raise ValidationError('Email is undeliverable')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateIngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    create = SubmitField('Create')


class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    text = StringField('Recipe Text', validators=[DataRequired()])
    ingredients = SelectMultipleField('Ingredient', validators=[DataRequired()],
                                      choices=[(ingredient.id, ingredient.name) for ingredient in Ingredient().list()],
                                      coerce=int)


class CreateRecipeForm(RecipeForm):
    create = SubmitField('Create')


class SearchRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name',)
    recipe_text = StringField('Recipe Text',)
    ingredients = SelectMultipleField('Ingredient',
                                      choices=[(ingredient.name, ingredient.name) for ingredient in Ingredient().list()],
                                      coerce=str)
    search = SubmitField('Search')
