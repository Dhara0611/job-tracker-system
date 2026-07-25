import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Application
from app.blueprints.applications.service import save_application,apply_job_service,get_applications_service, update_application_status_service, delete_application_service,get_application_status_service
from app.validators.decorators import validate_schema
from app.validators.schemas import JobCodeSchema, UpdateStatusSchema


logger = logging.getLogger(__name__)

application_bp = Blueprint("applications", __name__)


@application_bp.route("/save", methods=['POST'])
@jwt_required()
@validate_schema(JobCodeSchema)
def save_job(validated_data):

    try:
        user_id = get_jwt_identity()

        job_code = validated_data["job_code"]

        logger.info("[SAVE_JOB_START] user_id=%s job_code=%s", user_id, job_code)
        
        response, status_code = save_application(user_id, job_code)
        logger.info(
            "[SAVE_JOB_SUCCESS] user_id=%s job_code=%s status_code=%s",
            user_id,
            job_code,
            status_code
        )

        return jsonify(response), status_code
    
    except Exception as e:
        logger.exception(
            "[SAVE_JOB_ERROR] error=%s", str(e)
        )
        return jsonify({"error": "Internal server error"}), 500


@application_bp.route("/")
@jwt_required()
def get_applications():

    try:
        user_id =get_jwt_identity()
        status = request.args.get("status")

        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)

        logger.info(
            "[GET_APPLICATIONS_START] user_id=%s status=%s page=%s limit=%s",
            user_id,
            status,
            page,
            limit
        )

        response , status_code = get_applications_service(user_id,status,page,limit)
        logger.info(
            "[GET_APPLICATIONS_SUCCESS] user_id=%s status=%s page=%s limit=%s status_code=%s",
            user_id,
            status,
            page,
            limit,
            status_code
        )

        return jsonify(response), status_code
    
    except Exception as e:
        logger.exception(
            "[GET_APPLICATIONS_ERROR] user_id=%s error=%s",
            get_jwt_identity(),
            str(e)
        )

        return jsonify({
            "error": "Internal server error"
        }), 500




@application_bp.route("/apply", methods=["POST"])
@jwt_required()
@validate_schema(JobCodeSchema)
def apply_job(validated_data):

    try:
        user_id = get_jwt_identity()
        token = request.headers.get("Authorization")
        job_code = validated_data["job_code"]

        if not job_code:
            return jsonify({
                "error": "job_code is required"
            }),400

        logger.info("[APPLY_JOB_START] user_id=%s job_code=%s", user_id, job_code)
        
        response, status_code = apply_job_service(user_id, job_code,token)
        
        logger.info(
            "[APPLY_JOB_SUCCESS] user_id=%s job_code=%s status_code=%s",
            user_id,
            job_code,
            status_code
        )   

        return jsonify(response), status_code
    except Exception as e:
        logger.exception(
            "[APPLY_JOB_ERROR] user_id=%s job_code=%s error=%s",
            user_id,
            job_code,
            str(e)
        )
        return jsonify({"error": "Internal server error"}), 500


#this endpoint is only for recruiters. Recruiters can update the status of the application that is applied. 
@application_bp.route("/<job_code>/status",methods=["PATCH"])
@jwt_required()
@validate_schema(UpdateStatusSchema)
def update_application_status(job_code,validated_data):

    try:
        user_id = get_jwt_identity()
        
        claims = get_jwt()
        role = claims.get("role")
        logger.info(
            "[UPDATE_STATUS_START] recruiter_id=%s job_code=%s",
            user_id,
            job_code
        )

        #check the role of the user, if it is not recruiter then return error.
        if role != "recruiter":
            logger.warning(
                "[UPDATE_STATUS_FORBIDDEN] user_id=%s role=%s job_code=%s",
                user_id,
                role,
                job_code
            )
            return jsonify({
                "error": "Only recruiters can update application status"
            }), 403
        
        status = validated_data["status"]
        response, status_code = update_application_status_service(user_id, job_code, status)
        logger.info(
            "[UPDATE_STATUS_SUCCESS] recruiter_id=%s job_code=%s status=%s status_code=%s",
            user_id,
            job_code,
            status,
            status_code
        )

    except Exception as e:
        logger.exception( "[UPDATE_STATUS_ERROR] job_code=%s error=%s", job_code, status_code, str(e))
        return jsonify({
            "error": "Internal server error"
        }), 500


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


#user can delete the saved applications
@application_bp.route("/<job_code>", methods=["DELETE"])
@jwt_required()
def delete_application(job_code):

    try:
        user_id = get_jwt_identity()
        
        logger.info(
            "[DELETE_APPLICATION_START] user_id=%s job_code=%s",
            user_id,
            job_code
        )
        response, status_code = delete_application_service(user_id,job_code)

        logger.info(
            "[DELETE_APPLICATION_SUCCESS] user_id=%s job_code=%s",
            user_id,
            job_code
        )
        return jsonify(response), status_code
    except Exception as e:
        logger.exception(
            "[DELETE_APPLICATION_ERROR] user_id=%s job_code=%s error=%s",
            user_id,
            job_code,
            status_code,
            str(e)
        )
        return jsonify({
            "error": "Internal server error"
        }), 500