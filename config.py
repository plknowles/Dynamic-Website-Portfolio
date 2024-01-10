import os
import secrets

class Config:
    # SECRET_KEY = secrets.token_hex(16)
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(__file__), "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
