from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()

login_manager.login_view = 'login'
login_manager.init_app(app)

mail = Mail(app)

from app import models
from app.views import views

