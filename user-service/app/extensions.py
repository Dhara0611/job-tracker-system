#centralized shared resources
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#creating database object
db = SQLAlchemy()
migrate = Migrate()

