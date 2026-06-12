import logging
from flask import Flask, jsonify
from app.extensions import db, migrate,jwt
from app.config import Config
import app.models
from app.logging_config import setup_logging
from app.blueprints.applications import application_bp

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    setup_logging()
    app.config.from_object(Config)

    # initialize database object
    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    # blueprint registration
    app.register_blueprint(application_bp, url_prefix="/api/v1/applications")


    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify({"message": "Something went wrong"}), 500

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to application-service"})

    return app



