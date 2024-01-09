from flask import Flask
from blueprints import blueprints
from os import path
from database import db
from config import Config
from flask_login import LoginManager
from better_profanity import profanity
from flask_wtf.csrf import CSRFProtect
from models import Users, Comments

server = Flask(__name__)
server.config.from_object(Config)
db.init_app(server)
login_manager = LoginManager(server)

@login_manager.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

server.register_blueprint(blueprints, url_prefix = '/')

with server.app_context():
    if not path.exists("database.db"):
        print("Creating tables")
        try:
            db.create_all()
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")

    profanity.load_censor_words()
    csrf = CSRFProtect(server)

    login_manager.login_view = "blueprints.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(server)