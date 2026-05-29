import logging
from app.models import Job
from app.extensions import db

logger = logging.getLogger(__name__)

def get_all_jobs():
    logger.info("Loading all jobs")
    jobs = Job.query.all()

    # return list of job model objects
    return jobs

def search_jobs(q=None, title=None, company=None, location=None, page=1, limit=10):
    logger.info("Searching jobs")
    logger.debug("Search params: q=%s, title=%s, company=%s, location=%s, page=%s, limit=%s", q, title, company, location, page, limit)

    query = Job.query

    if title:
        query = query.filter(Job.title == title)

    if company:
        query = query.filter(Job.company == company)

    if location:
        query = query.filter(Job.location == location)

    if q:
        # ilike is used for case-insensitive search
        query = query.filter(
            db.or_(
                (Job.title.ilike(f"%{q}%")),
                (Job.company.ilike(f"%{q}%")),
                (Job.location.ilike(f"%{q}%"))
            )
        )

    # count the total number of records before applying offset and limit
    total = query.count()

    # pagination logic 
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    jobs = query.all()
    logger.info("Search returned %s jobs", len(jobs))
    return jobs, total

def generate_job_code(company_name):

    base = company_name.lower().replace(" ","-")

    count = Job.query.filter_by(company = company_name).count()
    new_count = count + 1
    job_code = base + "-" + str(new_count).zfill(2)

    return job_code


def create_job(data):
    logger.info("Creating job for company=%s title=%s", data.get("company"), data.get("title"))
    try:
        job = Job(
            job_code=generate_job_code(data["company"]),
            title=data["title"],
            company=data["company"],
            # optional fields: use .get() so missing values are handled gracefully
            location=data.get("location"),
            description=data.get("description")
        )
        db.session.add(job)
        db.session.commit()
        logger.info("Job created: %s", job.job_code)
        return job
    except Exception as e:
        db.session.rollback()
        logger.error("Failed to create job: %s", str(e), exc_info=True)
        raise

def get_job_by_code(code):
    return Job.query.filter_by(job_code=code).first()

