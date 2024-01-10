# database models created using SQLAlchemy
# Flask-SQLAlchemy has built-in support for parameterized queries, instead of formatting SQL queries manually. Prevents SQL Injection.
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # UserMixin required by Flask-Login for user authentication and allows a get_id method
from datetime import datetime
from flask_bcrypt import Bcrypt # bcrypt used to hash passwords for improved data protection and security
from database import db

# Create an instance of bcrypt for password hashing
bcrypt = Bcrypt()

# User model for authentication
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(150), nullable = False)

# Comments model to store user comments
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    text = db.Column(db.String(10000), nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = datetime.now, nullable = False)

    # Define foreign key relationships with the Users table
    user_name = db.Column(db.String(150), db.ForeignKey("users.name"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    # Define the relationship with the Users table
    user = db.relationship("Users", backref = "comments", foreign_keys = [user_id])