from flask import Flask
from server_blueprints import blueprints
from os import path
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "pass"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, "database.db")}'
db.init_app(app)

app.register_blueprint(blueprints, url_prefix='/')

from models import Users, Comments

if __name__ == "__main__":
    with app.app_context():
        if not path.exists("database.db"):
            db.create_all()
    app.run(debug=True)
