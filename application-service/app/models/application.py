from datetime import datetime
from app.extensions import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # comes from JWT (user-service)
    user_id = db.Column(db.Integer, nullable=False)

    # job reference from job-service
    job_code = db.Column(db.String(50), nullable=False)

    # status tracking
    status = db.Column(
        db.String(20),
        nullable=False,
        default="SAVED"
    )

    created_at = db.Column(
    db.DateTime(timezone=True),
    server_default=db.func.current_timestamp()
    )

    updated_at = db.Column(
    db.DateTime(timezone=True),
    server_default=db.func.now(),
    onupdate=db.func.now()
    )

    # prevent duplicate applications
    #It defines table-level constraints, not column-level constraints.
    __table_args__ = (
        db.UniqueConstraint("user_id", "job_code", name="unique_user_job"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_code": self.job_code,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

"""
to_dict() is used to convert your database model into a JSON-friendly dictionary 
so it can be safely returned from Flask APIs.
"""