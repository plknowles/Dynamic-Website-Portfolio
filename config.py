import os

class Config:
    SECRET_KEY = "pass"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(__file__), "database.db")}'
