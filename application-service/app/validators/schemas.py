from marshmallow import Schema, fields , validate

class JobCodeSchema(Schema):

    job_code = fields.String(required=True)

class UpdateStatusSchema(Schema):

    status = fields.String(required=True,
        validate=validate.OneOf([
            "SAVED",
            "APPLIED",
            "INTERVIEW",
            "ARCHIVED"
        ])
    )

