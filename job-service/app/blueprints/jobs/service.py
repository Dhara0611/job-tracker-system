from app.models import Job
from app.extensions import db

def get_all_jobs():
    jobs = Job.query.all()

    #return list of job model objects
    return jobs

def search_jobs(q=None, title=None, company=None, location=None, page=1, limit=10):

    query = Job.query

    if title:
        query = query.filter(Job.title == title)

    if company:
        query = query.filter(Job.company == company)

    if location:
        query = query.filter(Job.location == location)

    if q:
#ilike is used for case-insensitive search
        query = query.filter(
            db.or_(
            (Job.title.ilike(f"%{q}%")),
            (Job.company.ilike(f"%{q}%")),
            (Job.location.ilike(f"%{q}%"))
        ))

    
#count the total number of records before applying offset and limit
    total = query.count()

#pagination logic 
    offset = (page - 1)*limit
    query = query.offset(offset).limit(limit)
    jobs = query.all()
    return jobs, total

def generate_job_code(company_name):

    base = company_name.lower().replace(" ","-")

    count = Job.query.filter_by(company = company_name).count()
    new_count = count + 1
    job_code = base + "-" + str(new_count).zfill(2)

    return job_code


def create_job(data):
    
    job = Job(
        job_code = generate_job_code(data["company"]),
        title = data["title"],
        company=data["company"],
        location=data.get("location")
    )
    db.session.add(job)
    db.session.commit()

    return job

def get_job_by_code(code):
    return Job.query.filter_by(job_code=code).first()

