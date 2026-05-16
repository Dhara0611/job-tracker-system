from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.blueprints.preferences.services import upsert, get_preferences_service
from app.validators.preferences_validator import PreferencesSchema
from app.validators.decorators import validate_schema
import logging

pref_bp = Blueprint("preferences", __name__)

logger = logging.getLogger(__name__)

@pref_bp.route("/",methods=["POST"])
@jwt_required()
@validate_schema(PreferencesSchema)
def save_preference(validated_data):
    
    user_id = get_jwt_identity()
    # data = request.get_json()

    response, status_code = upsert(user_id,validated_data)
    return jsonify(response), status_code


@pref_bp.route("/",methods=["GET"])
@jwt_required()
def get_preferences():
    
    user_id = get_jwt_identity()
    response, status_code = get_preferences_service(user_id)
    return jsonify(response), status_code


#endpoint to test error handling
@pref_bp.route("/test-logs", methods=["GET"])
def test_logs():

    logger.info("This is an INFO log")
    logger.warning("This is a WARNING log")
    logger.error("This is an ERROR log")
    logger.debug("This is a DEBUG log")

    return {"message": "Logs generated"}, 200