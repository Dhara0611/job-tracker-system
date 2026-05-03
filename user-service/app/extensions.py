#centralized shared resources
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

#creating database object
db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
JWT_SECRET_KEY = "super-secret-key"


