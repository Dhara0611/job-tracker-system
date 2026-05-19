from app.extensions import db
from datetime import datetime

class Preference(db.Model):
    __tablename__ = "preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique = True)
    role = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    location = db.Column(db.String(100))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)

    created_at = db.Column(db.DateTime(timezone=True), server_default = db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default = db.func.now(),
                            onupdate=db.func.now()) 

"""
server_default: Writes the default value rule straight into your database schema migrations, making it 
independent of Flask.

DateTime(timezone=True): Forces the database backend (like PostgreSQL) 
to track global timezone offsets properly.

onupdate=db.func.now() - Auto update this column whenever row is updated
"""