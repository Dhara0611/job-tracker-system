from marshmallow import Schema, fields, validate


class JobSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=2, max=255))
    company = fields.String(required=True, validate=validate.Length(min=2, max=255))
    location = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))
    description = fields.String(required=False, allow_none=True)
