from flask import Flask,jsonify
from app.extensions import db,migrate
from app.config import Config
import app.models

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    #initialize database object
    db.init_app(app)
    migrate.init_app(app,db)

    
    @app.route("/")
    def home():
        return jsonify({
                "message":"Welcome to job-service"
            })
    return app

