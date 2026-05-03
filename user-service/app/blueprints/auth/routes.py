from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

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
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "error" : "User already exists"
        }), 400
    
    try:
        #password hashing algorithm designed for security
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message" : "User registered successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "error" : str(e)
            }
        ), 500


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

    #find the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    #check the password
    if not check_password_hash(user.password, password):
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    #create access token
    #JWT requires sub (subject) to be a string
    token = create_access_token(identity=str(user.id))
    return jsonify({
            "message": "Login successfull",
            "access_token": token
        }), 200

#returns the details of the user and only accessible if user sends access token
@auth_bp.route("/profile")
@jwt_required()
def profile():
    
    #get_jwt_identity extracts the id from the token
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "user not found"
        }), 404
    
    return jsonify({
            "id" : user.id,
            "email": user.email
        }), 200



        
    
   

