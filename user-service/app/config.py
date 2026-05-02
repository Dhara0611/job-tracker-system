#Central place for all environment-based settings.
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","dev-secret")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///dev.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False