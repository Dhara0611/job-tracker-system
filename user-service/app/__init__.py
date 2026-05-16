from flask import Flask, jsonify
import logging
from app.config import Config
from app.extensions import db, migrate,jwt
import app.models
from app.blueprints.auth import auth_bp
from app.blueprints.preferences import pref_bp
from app.logging_config import setup_logging
from app.utils.exceptions import ValidationError

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    #setup logging whenever the app starts
    setup_logging()

    #handle user error first
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logger.warning(f"Validation error: {e.message}")
        return jsonify({
            "message" : e.message
        }), e.status_code

    #setup a global error handler for unhandled exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):

        logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({
            "message": "Something went wrong"
        }), 500
    
#load configuration here
#from_object is a Flask method and says - take a python class config and copy its attributes into 
#app.config

    app.config.from_object(Config)

    #initialize extensions
    #attaching it to app to use the app config and to become active
    db.init_app(app)

    #connects Flask + DB + migration system
    migrate.init_app(app, db)
    jwt.init_app(app)

    #Blueprint registration
    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(pref_bp, url_prefix = "/preferences")

    

    @app.route("/")
    def home():
        return {"message":"user is running (factory pattern)"}

    return app
    