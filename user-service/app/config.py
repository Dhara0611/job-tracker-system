#Central place for all environment-based settings.
#.env is just storage, load_dotenv loads it into the system, os.getenv reads it
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")