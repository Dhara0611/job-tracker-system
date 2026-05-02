from flask import Flask
from app.config import Config
from app.extensions import db, migrate
import app.models

def create_app():
    app = Flask(__name__)

#load configuration here
#from_object is a Flask method and says - take a python class config and copy its attributes into 
#app.config

    app.config.from_object(Config)

    #initialize extensions
    #attaching it to app to use the app config and to become active
    db.init_app(app)

    #connects Flask + DB + migration system
    migrate.init_app(app, db)

    @app.route("/")
    def home():
        return {"message":"user is running (factory pattern)"}

    return app
    