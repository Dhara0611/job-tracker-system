from app.models import Application
from app.extensions import db
import logging
from app.clients.job_service import get_job_details

logger = logging.getLogger(__name__)


def save_application(user_id, job_code):

    try:  
        #check if job_code already exists in Applications table, if so check the status and send appropriate mesaage
        #without this same user saves same job 10 times → 10 rows
        existing = Application.query.filter_by(
                    user_id=user_id,
                    job_code=job_code
                    ).first()

        if existing:
            if existing.status == "SAVED":
                return{
                    "message": "Job already saved",
                    "data" : existing.to_dict()
                }, 200
            if existing.staus == "APPLIED":
                return{
                    "message": "Applied jobs cannot be saved again",
                    "data" : existing.to_dict()
                }, 400 
        
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
    
    except Exception as e:
        db.session.rollback()
        logger.exception(
            "[SAVE_APPLICATION_SERVICE_ERROR] user_id=%s job_code=%s error=%s",
            user_id,
            job_code,
            str(e)
        )
        raise e



def get_applications_service(user_id, status=None, page=1,limit=10):
    
    try:
        logger.info(
            "[GET_APPLICATIONS_SERVICE_START] user_id=%s status=%s page=%s limit=%s",
            user_id,
            status,
            page,
            limit
        )
        # Fetch applications only for the logged-in user
        query = Application.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)
        
        """
            Pagination:
            paginate divides the results into smaller pages.
        
            page -> which page of results we want
            limit -> number of records per page
        
            Example:
            page=1, limit=10 -> first 10 applications
            page=2, limit=10 -> next 10 applications
        """
        # error_out=False prevents an error if requested page does not exist

        if page < 1:
            page = 1

        if limit > 50:
            limit = 50
            
        paginated_applications = query.paginate(
            page=page,
            per_page = limit,
            error_out=False
        )

        # .items contains only the records for the current page
        applications = paginated_applications.items

        respone={
            "message" : "Applications fetched successfully",
            "data" : [app.to_dict() for app in applications],
            # Pagination metadata helps frontend know:
            # current page, page size, total records and total pages
            "pagination":{
                "page": page,
                "limit": limit,
                "total_items": paginated_applications.total,
                "total_pages": paginated_applications.pages
            }
        }

        logger.info(
            "[GET_APPLICATIONS_SERVICE_SUCCESS] user_id=%s status=%s count=%s",
            user_id,
            status,
            len(applications)
        )

        return respone, 200
    
    except Exception as e:
        logger.exception(
            "[GET_APPLICATIONS_SERVICE_ERROR] user_id=%s status=%s error=%s",
            user_id,
            status,
            str(e)
        )
        raise e


# def apply_job_service(user_id, job_code):
#     try:
#         logger.info(
#             "[APPLY_JOB_SERVICE_START] user_id=%s job_code=%s",
#             user_id,
#             job_code
#         )
#         existing = Application.query.filter_by(
#             user_id=user_id,
#             job_code=job_code
#         ).first()

#         # CASE 1: already exists → update status
#         if existing:
#             if existing.status == "SAVED":
#                 existing.status == "APPLIED"
#                 db.session.commit()

#                 logger.info(
#                     "[APPLY_JOB_SERVICE_UPDATED] user_id=%s job_code=%s",
#                     user_id,
#                     job_code
#                 )
#                 return {
#                     "message": "Job marked as applied",
#                     "data": existing.to_dict()
#                 }, 200
        
#             return {
#                     "message": f" Application already in {existing.status} status ",
#                     "data": existing.to_dict()
#                 }, 400

#         # CASE 2: not exists → create new record

#         application = Application(
#             user_id=user_id,
#             job_code=job_code,
#             status="APPLIED"
#         )

#         db.session.add(application)
#         db.session.commit()

#         logger.info(
#                 "[APPLY_JOB_SERVICE_SUCCESS] user_id=%s job_code=%s",
#                 user_id,
#                 job_code
#                 )

#         return {
#             "message": "Job applied successfully",
#             "data": application.to_dict()
#         }, 201
    
#     except Exception as e:
#         db.session.rollback()

#         logger.exception(
#             "[APPLY_JOB_SERVICE_ERROR] user_id=%s job_code=%s error=%s",
#             user_id,
#             job_code,
#             str(e)
#         )
#         raise e

def update_application_status_service(user_id, job_code , status):
    try:

        logger.info(
            "[UPDATE_APPLICATION_STATUS_START] user_id=%s job_code=%s",
            user_id,
            job_code
        )
        application = Application.query.filter(
                                            job_code = job_code
                                            ).first()
        
        if not application:
            return{
                "message" : "application not found"
            },404
        
        #check the current status of the application, it should be applied
        if application.status != "APPLIED":
            logger.warning(
                "[UPDATE_APPLICATION_STATUS_INVALID_CURRENT_STATUS] job_code=%s current_status=%s",
                job_code,
                application.status
            )

            return{
                "message": "Only applied applications can be updated"
            },400
        
        # validate new status
        allowed_status = [
            "INTERVIEW",
            "ARCHIVED",
            "OFFER"
        ]

        if status not in allowed_status:
            
            logger.warning(
                "[UPDATE_APPLICATION_STATUS_INVALID_NEW_STATUS] job_code=%s status=%s",
                job_code,
                status
            )
            return {
                "message": "Invalid status"
            }, 400
        
        #update the status of the applied application
        application.status = status
        db.session.commit()
        logger.info(
                "[UPDATE_APPLICATION_STATUS_SUCCESS] job_code=%s status=%s",
                job_code,
                status
            )
        return{
            "message":"Application status updated successfully",
            "data" : application.to_dict()
        },200
    
    except Exception as e:

        db.session.rollback()
        logger.exception(
            "[UPDATE_APPLICATION_STATUS_ERROR] user_id=%s job_code=%s error=%s",
            user_id,
            job_code,
            str(e)
        )
        raise e

def apply_job_service(user_id, job_code,token):

#call to job-service to check if the job is open or closed. If it is closed, user should not apply
    try:
        logger.info(
            "[APPLY_JOB_SERVICE_START] user_id=%s job_code=%s",
            user_id,
            job_code
        )
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
    
    except Exception as e:
            db.session.rollback()
    
            logger.exception(
                "[APPLY_JOB_SERVICE_ERROR] user_id=%s job_code=%s error=%s",
                user_id,
                job_code,
                str(e)
            )
            raise e
def delete_application_service(user_id, job_code):
    try:
        logger.info(
            "[DELETE_APPLICATION_SERVICE_START] user_id=%s job_code=%s",
            user_id,
            job_code
        )

        application = Application.query.filter_by(
            user_id=user_id,
            job_code=job_code
        ).first()

        #CASE1: Application not found
        if not application:
            logger.warning(
                "[DELETE_APPLICATION_NOT_FOUND] user_id=%s job_code=%s",
                user_id,
                job_code
            )

            return {
                "message": "Application not found"
            }, 404

        # BUSINESS RULE
        # CASE2:only SAVED can be deleted
        if application.status != "SAVED":
            logger.warning(
                "[DELETE_APPLICATION_BLOCKED] user_id=%s job_code=%s status=%s",
                user_id,
                job_code,
                application.status
            )

            return {
                "message": "Only saved applications can be deleted"
            }, 400
        # CASE3: Delete the application
        db.session.delete(application)
        db.session.commit()

        logger.info(
            "[DELETE_APPLICATION_SUCCESS] user_id=%s job_code=%s",
            user_id,
            job_code
        )

        return {
            "message": "Application deleted successfully"
        }, 200
    
    except Exception as e:
        db.session.rollback()
        logger.exception(
            "[DELETE_APPLICATION_ERROR] user_id=%s job_code=%s error=%s",
            user_id,
            job_code,
            str(e)
        )
        raise e

def get_application_status_service(user_id):

    applications = Application.query.filter_by(user_id = user_id).all()
    status_map ={}

    for application in applications:
        status_map[application.job_code] = application.status

    return{
        "mesaage": "Applications statuses fetched successfully",
        "data": status_map
    },200

