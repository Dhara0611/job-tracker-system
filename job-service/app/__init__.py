from flask import Flask,jsonify
from app.extensions import db,migrate
from app.config import Config
import app.models
from app.blueprints.jobs.routes import jobs_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    #initialize database object
    db.init_app(app)
    migrate.init_app(app,db)

    #blueprint registration
    app.register_blueprint(jobs_bp, url_prefix = "/api/v1/jobs")



    @app.route("/")
    def home():
        return jsonify({
                "message":"Welcome to job-service"
            })
    return app



