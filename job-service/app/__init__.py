from flask import Flask,jsonify
from app.extensions import db,migarte
from app.config import Config
import app.models

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    #initialize database object
    db.init_app(app)
    migarte.init_app(app,db)

    
    @app.route("/")
    def home():
        return jsonify({
                "message":"Welcome to job-service"
            })
    return app

