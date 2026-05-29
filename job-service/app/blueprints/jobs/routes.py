import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.blueprints.jobs.service import get_all_jobs, create_job, get_job_by_code, search_jobs
from app.models import Job
from app.extensions import db
from app.validators.job_validator import JobSchema
from app.validators.decorators import validate_schema

logger = logging.getLogger(__name__)

jobs_bp = Blueprint("jobs", __name__)

# @jobs_bp.route("/")
# def test():
#     return jsonify(
#         {
#             "message" : "Welcome to jobs-service blueprint"
#         }
#     ), 200

@jobs_bp.route("/")
def get_jobs():
    logger.info("Fetching job list")

    # get the query parameters 
    q = request.args.get("q")
    title = request.args.get("title")
    company = request.args.get("company")
    location = request.args.get("location")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    logger.debug("Search params: q=%s, title=%s, company=%s, location=%s, page=%s, limit=%s", q, title, company, location, page, limit)
    jobs, total = search_jobs(q, title, company, location, page, limit)

    list_of_jobs = []
    
#job is object of Job model class
    for job in jobs:
        
        required_job_details = {
            "job_code" : job.job_code,
            "title" : job.title,
            "company" : job.company,
            "location" : job.location,
        #adding status after adding it to the model
            "status": job.status
        }
        list_of_jobs.append(required_job_details)

#calculate number of pages 
    
    pages = (total + limit - 1) // limit

    return jsonify({
        "success" : "true",
        "message" : "Jobs fetched successfully",
        "data" : list_of_jobs,
        "meta":{
            "page"  : page,
            "limit" : limit,
            "total" : total, 
            "pages" : pages
        }

    }), 200

#endpoint to add a job
@jobs_bp.route("/", methods=["POST"])
@validate_schema(JobSchema)
def add_job(validated_data):
    logger.info("Creating new job: %s at %s", validated_data.get("title"), validated_data.get("company"))
    job = create_job(validated_data)
    logger.info("Created job %s", job.job_code)
    return jsonify(
        {
            "job_code": job.job_code,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            # adding status after adding it to the model
            "status": job.status
        }
    ), 201

@jobs_bp.route("/<job_code>", methods=["GET"])
def get_job(job_code):

    job = get_job_by_code(job_code)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    return jsonify({
        "job_code": job.job_code,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "status": job.status
    }), 200


@jobs_bp.route("/<job_code>/close", methods=["PATCH"])
@jwt_required()
def close_job(job_code):
    #check is the user is a recruiter
    
    claims = get_jwt()
    if claims.get("role") != "recruiter":
        return jsonify({
            "error": "Recruiter access required to close the job"
        }), 403
    
    #find the job by job code
    job = Job.query.filter_by(job_code=job_code).first()

    if not job:
        return jsonify({
            "error" : "Job not found "
        }), 404

    #close the job and return the details
    job.status = "CLOSED"
    db.session.commit()
    return jsonify({
        "message" : "Job closed successfully",
        "job code" : job.jobcode,
        "status" : job.status
    }),200



    


