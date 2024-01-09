from flask import Flask
from blueprints import blueprints
from os import path
from database import db
from config import Config
from flask_login import LoginManager
from better_profanity import profanity
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

app.register_blueprint(blueprints, url_prefix = '/')

from models import Users, Comments

if __name__ == "__main__":        
    with app.app_context():
        if not path.exists("database.db"):
            db.create_all()
    profanity.load_censor_words()
    csrf = CSRFProtect(app)
    
    login_manager.login_view = "blueprints.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
    
    # app.run(debug = True)