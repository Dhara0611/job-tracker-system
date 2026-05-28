from datetime import datetime
from app.extensions import db

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    job_code = db.Column(db.String(20), unique=True, nullable = False)

    #job details
    title = db.Column(db.String(255),nullable = False)
    company = db.Column(db.String(255),nullable = False)
    location = db.Column(db.String(255),nullable = True)
    description = db.Column(db.Text,nullable = True)
    created_at = db.Column(db.DateTime(timezone=True), server_default = db.func.now())
#adding status column to job model
    status = db.Column(db.String(20), nullable=False, server_default="OPEN")