from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from database import db

bcrypt = Bcrypt()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(150), nullable = False)
    comment = db.relationship("Comments")

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    text = db.Column(db.String(10000), nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = func.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))