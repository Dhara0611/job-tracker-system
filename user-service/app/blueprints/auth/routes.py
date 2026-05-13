from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.blueprints.auth.services import create_user, authenticate_user, get_user_profile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    #check if data is not empty
    if not email or not password:
        return jsonify({
            "error": "Email or password are required"
        }), 400
    
    #check is user already exists
    response , status_code = create_user(email, password)
    return jsonify(response), status_code
    

@auth_bp.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    #check if data is not empty
    if not email or not password:
        return jsonify({
            "error": "Email or password are required"
        }), 400

 
    response, status_code = authenticate_user(email,password)

    return jsonify(response), status_code



#returns the details of the user and only accessible if user sends access token
@auth_bp.route("/profile")
@jwt_required()
def profile():
    
    #get_jwt_identity extracts the id from the token
    user_id = get_jwt_identity()

    response, status_code = get_user_profile(user_id)
    return jsonify(response), status_code



        
    
   

