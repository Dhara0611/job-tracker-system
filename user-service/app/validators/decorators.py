from functools import wraps
from flask import request, jsonify

def validate_schema(schema_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            data = request.get_json()

#creating an instance of schema class
            schema = schema_class()
            errors = schema.validate(data)

            if errors:
                return jsonify(errors), 400

            kwargs["validated_data"] = data

            return func(*args, **kwargs)

        return wrapper
    return decorator