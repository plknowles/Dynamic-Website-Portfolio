from flask import Flask
from blueprints import blueprints
from os import path
from database import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(blueprints, url_prefix='/')

from models import Users, Comments

if __name__ == "__main__":
    with app.app_context():
        if not path.exists("database.db"):
            db.create_all()
    app.run(debug=True)
