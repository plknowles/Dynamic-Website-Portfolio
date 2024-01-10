from flask import Flask
from blueprints import blueprints
from os import path
from database import db
from config import Config
from flask_login import LoginManager
from better_profanity import profanity # https://github.com/snguyenthanh/better_profanity
from flask_wtf.csrf import CSRFProtect
from models import Users, Comments

# Create a Flask application
server = Flask(__name__)
server.config.from_object(Config)
db.init_app(server)
login_manager = LoginManager(server)

# Load the user for Flask-Login
@login_manager.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

# Register blueprints
server.register_blueprint(blueprints, url_prefix = '/')

with server.app_context():
    # Create database tables if don't exist
    if not path.exists("database.db"):
            db.create_all()

    # Load profanity filter
    profanity.load_censor_words()
    csrf = CSRFProtect(server)
    csrf.init_app(server)

    # Configure Flask-Login
    login_manager.login_view = "blueprints.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(server)

# if __name__ == "__main__": # commented out as using gunicorn to serve flask
#     server.run(debug = True)
