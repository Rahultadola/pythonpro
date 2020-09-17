from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from videosurfing.config import Config

login_manager = LoginManager()
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
	


def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from videosurfing.users.routes import users
	from videosurfing.vidPosts.routes import vidPost
	from videosurfing.main.routes import main
	from videosurfing.errors.handlers import errors
	

	app.register_blueprint(users)
	app.register_blueprint(vidPost)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app