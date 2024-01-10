import os
import secrets

class Config:
    # SECRET_KEY = secrets.token_hex(16) # this wasn't allowing me to deploy to OpenShift for some reason
    SECRET_KEY = "42db308d17d056e7bc1b095d6a0ba6c9"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(__file__), "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
