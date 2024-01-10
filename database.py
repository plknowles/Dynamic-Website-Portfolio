# I've defined the SQLAlchemy database object in here to prevent issues with circular imports when it was in other files
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
