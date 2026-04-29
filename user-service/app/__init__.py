from flask import Flask
from app.config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)

#load configuration here
#from_object is a Flask method and says - take a python class config and copy its attributes into 
#app.config

    app.config.from_object(Config)

    #initialize extensions
    db.init_app(app)

    @app.route("/")
    def home():
        return {"message":"user is running (factory pattern)"}

    return app
    