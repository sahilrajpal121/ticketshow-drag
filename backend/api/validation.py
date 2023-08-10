from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class SchemaValidationError(HTTPException):
    def __init__(self, status_code, error_code, message):
        data = {"error_code": error_code, "message": message}
        self.response = make_response(json.dumps(data), status_code)


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, message):
        data = {"error_code": error_code, "message": message}
        self.response = make_response(json.dumps(data), status_code)


class NotFoundError(HTTPException):
    def __init__(self, message, status_code=404):
        data = {"message": message}
        self.response = make_response(json.dumps(data), status_code)


class PropertyExistError(HTTPException):
    def __init__(self, status_code, message):
        data = {"message": message}
        self.response = make_response(json.dumps(data), status_code)
