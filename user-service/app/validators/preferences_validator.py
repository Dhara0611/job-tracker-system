from marshmallow import Schema, fields, validate

class PreferencesSchema(Schema):
    role=fields.String(required=True, validate=validate.Length(min=2,max=100))

    experience=fields.String(required=False, allow_none=True)
    location=fields.String(required=False, allow_none=True)
    salary_min=fields.Integer(required=False, allow_none=True)
    salary_max=fields.Integer(required=False,allow_none=True)

"""
Allow-none = True 
It tells Marshmallow: This field is allowed to have value None (JSON null).
"""

