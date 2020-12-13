from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_access_cookies, \
    jwt_refresh_token_required
from flask import render_template, Blueprint, redirect, url_for, flash, request, make_response
from factoryworldwide_app.forms.Forms import RegistrationForm, LoginForm

from factoryworldwide_app.services.UserService import UserService
from factoryworldwide_app.server import app

auth = Blueprint('auth', __name__, template_folder='../templates')
jwt = JWTManager(app)


@jwt.unauthorized_loader
def my_exipired_token_callback(expired_token):
    flash('Valid token needed')
    return redirect(url_for('auth.logout'))


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    flash('Valid token needed')
    return redirect(url_for('auth.logout'))


@jwt.invalid_token_loader
def my_invalid_token_callback(invalid_token):
    flash('Valid token needed')
    return redirect(url_for('auth.logout'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        UserService.create_user(data)
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        if UserService.login(data):
            access_token = create_access_token(identity=data['email'])
            response = make_response(redirect(url_for('web.home')))
            set_access_cookies(response, access_token)

            return response

        else:
            flash('Invalid email or password.')

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login')))
    unset_access_cookies(response)
    # UserService().logout()
    flash('You have successfully been logged out.')
    return response
