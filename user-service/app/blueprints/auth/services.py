from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


def create_user(email, password):
    #check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {
            "error" : "User already exists"
        }, 400
    
    try:
        #password hashing algorithm designed for security
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return {
            "message" : "User registered successfully"
        }, 201
    except Exception as e:
        db.session.rollback()
        return {
                "error" : str(e)
            }, 500

def authenticate_user(email, password):
    #find the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return {
            "error": "Invalid credentials"
        }, 401

    #check the password
    if not check_password_hash(user.password, password):
        return {
            "error": "Invalid credentials"
        }, 401

    #create access token
    #JWT requires sub (subject) to be a string
    token = create_access_token(identity=str(user.id))
    return {
            "message": "Login successfull",
            "access_token": token
        }, 200

def get_user_profile(user_id):

    user = User.query.get(user_id)

    if not user:
        return {
            "error": "user not found"
        }, 404
    
    return {
            "id" : user.id,
            "email": user.email
        }, 200
