from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.blueprints.auth.services import create_user, authenticate_user, get_user_profile
from app.validators.auth_validator import RegisterSchema , LoginSchema 
from app.validators.decorators import validate_schema

auth_bp = Blueprint('auth', __name__)

# Decorators are applied bottom → top (execution flows top → bottom)
# Route should be outermost, followed by validation/auth decorators

@auth_bp.route("/register", methods=["POST"])
@validate_schema(RegisterSchema)
def register(validated_data):
    # data = request.get_json()

    email = validated_data.get("email")
    password = validated_data.get("password")

    #check is user already exists

    response , status_code = create_user(email, password)
    return jsonify(response), status_code
    

@auth_bp.route("/login", methods=["POST"])
@validate_schema(LoginSchema)
def login(validated_data):
    
    # data = request.get_json()

    email = validated_data.get("email")
    password = validated_data.get("password")

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



        
    
   

