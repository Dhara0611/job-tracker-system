from flask import Flask,jsonify
from app.extensions import db

def create_app():
    app = Flask(__name__)


    #initialize database object
    db.init_app(app)

    
    @app.route("/")
    def home():
        return jsonify({
                "message":"Welcome to job-service"
            })
    return app

