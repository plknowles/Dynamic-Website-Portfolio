from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from flask_bcrypt import Bcrypt
from database import db

bcrypt = Bcrypt()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(150), nullable = False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    text = db.Column(db.String(10000), nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = datetime.now, nullable = False)

    user_name = db.Column(db.String(150), db.ForeignKey("users.name"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    # Define the relationship with the Users table
    user = db.relationship("Users", backref = "comments", foreign_keys = [user_id])