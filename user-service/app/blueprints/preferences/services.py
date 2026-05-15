from app.models.preferences import Preference
from app.extensions import db

def upsert(userid, data):
    
    pref = Preference.query.filter_by(user_id=userid).first()

    if not pref:
        pref = Preference(user_id = userid)
#only update the fields that are present in the request
#otherwise if fields are empty they will override the database

    if "role" in data:
        pref.role = data["role"]

    if "experience" in data:
        pref.experience = data["experience"]

    if "location" in data:
        pref.location = data["location"]

    if "salary_min" in data:
        pref.salary_min = data["salary_min"]

    if "salary_max" in data:
        pref.salary_max = data["salary_max"]

    db.session.add(pref)
    db.session.commit()

    return{
        "message" : "Preferences saved successfully"
    },200

def get_preferences_service(userid):
    pref = Preference.query.filter_by(user_id=userid).first()

    if not pref:
        return{
            "error":"Preferences not found"
        },404
    
    return{
        "role" : pref.role,
        "experience":pref.experience,
        "location":pref.location,
        "salary_min":pref.salary_min,
        "salary_max":pref.salary_min
            },200