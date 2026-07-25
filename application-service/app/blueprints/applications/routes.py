import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Application
from app.extensions import db
from app.blueprints.applications.service import save_application,apply_job_service,get_applications_service, get_application_status_service

logger = logging.getLogger(__name__)

application_bp = Blueprint("applications", __name__)


@application_bp.route("/save", methods=['POST'])
@jwt_required()
def save_job():

    user_id = get_jwt_identity()

    data = request.get_json()
    job_code = data.get("job_code")

    if not job_code:
        return jsonify({"error": "job_code is required"}), 400
    
    response, status_code = save_application(user_id, job_code)
    return jsonify(response), status_code


@application_bp.route("/")
@jwt_required()
def get_applications():

    user_id =get_jwt_identity()
    status = request.args.get("status")

    response , status_code = get_applications_service(user_id,status)
    return jsonify(response), status_code



@application_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_job():

    user_id = get_jwt_identity()
    token = request.headers.get("Authorization")

    data = request.get_json()
    job_code = data.get("job_code")


    if not job_code:
        return jsonify({
            "error": "job_code is required"
        }),400
    
    response, status_code = apply_job_service(user_id, job_code,token)

    return jsonify(response), status_code


#internal endpoint for other services 
@application_bp.route("/user-status")
@jwt_required()
def get_user_application_status():
    try:
        user_id = get_jwt_identity()
        logger.info(
            "[GET_APPLICATION_STATUS_START] user_id=%s",
            user_id
        )

        response, status_code = get_application_status_service(user_id)

        return jsonify(response), status_code

    except Exception as e:
        logger.exception(
            "[GET APPLICATION STATUS ERROR] user_id=%s error=%s",
            user_id,
            str(e)
        )
        return jsonify({
            "error": "Internal server error"
        }),500
