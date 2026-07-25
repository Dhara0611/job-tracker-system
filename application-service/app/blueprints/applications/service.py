from app.models import Application
from app.extensions import db
from app.clients.job_service import get_job_details

def save_application(user_id, job_code):
        
    #check if job_code already exists in Applications table, if so update again to save status and commit
    #without this same user saves same job 10 times → 10 rows
    existing = Application.query.filter_by(
                user_id=user_id,
                job_code=job_code
                ).first()

    if existing:
        existing.status = "SAVED"
        db.session.commit()

        return {
            "message": "Job already saved",
            "data": existing.to_dict()
        }, 200
    
    #if it new job_code, add the application in the applications table with status as SAVE

    application = Application(
                    user_id=user_id,
                    job_code=job_code,
                    status="SAVED"
                )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Job saved successfully",
        "data": application.to_dict()
    }, 201

# def get_saved_jobs(user_id):

#     saved_jobs = Application.query.filter_by(
#         user_id=user_id,
#         status="SAVED"
#     ).all()
#     return {
#         "message" : "Saved jobs fetched successfully",
#         "data" : [job.to_dict() for job in saved_jobs]
#     }

def get_applications_service(user_id, status=None):
    
    query = Application.query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)
    
    applications = query.all()
    return{
        "message" : "Applications fetched successfully",
        "data" : [app.to_dict() for app in applications]
    },200

def apply_job_service(user_id, job_code,token):

#call to job-service to check if the job is open or closed. If it is closed, user should not apply
    job = get_job_details(job_code,token)
    if not job:
        return {
            "message": "Job not found"
        },404


    if job["status"] == "CLOSED":
        return {
            "message": "Cannot apply to closed job"
        },400
    
    existing = Application.query.filter_by(
        user_id=user_id,
        job_code=job_code
    ).first()

    # CASE 1: already exists → update status
    if existing:
        existing.status = "APPLIED"
        db.session.commit()

        return {
            "message": "Job marked as applied",
            "data": existing.to_dict()
        }, 200

    # CASE 2: not exists → create new record
    application = Application(
        user_id=user_id,
        job_code=job_code,
        status="APPLIED"
    )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Job applied successfully",
        "data": application.to_dict()
    }, 201

def get_application_status_service(user_id):

    applications = Application.query.filter_by(user_id = user_id).all()
    status_map ={}

    for application in applications:
        status_map[application.job_code] = application.status

    return{
        "mesaage": "Applications statuses fetched successfully",
        "data": status_map
    },200