from flask import Flask
from flask_login import LoginManager
from pyhunter import PyHunter
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy

DEBUG = True

app = Flask(__name__)
# api = Api(app)

app.config.from_pyfile('../config/LocalConfig.py')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "web.login"
bootstrap = Bootstrap(app)

EMAILHUNTER_API_KEY = '438b7edcca5e91160ec150214c0bea197ddf2665'
hunter = PyHunter(EMAILHUNTER_API_KEY)
