from flask import Flask
from blueprints import blueprints
from os import path
from database import db
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(blueprints, url_prefix='/')

from models import Users, Comments

if __name__ == "__main__":
    with app.app_context():
        if not path.exists("database.db"):
            db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = "blueprints.login"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    
    app.run(debug=True)

