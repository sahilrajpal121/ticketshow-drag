from flask_restful import Resource, reqparse, marshal_with, fields
from flask import jsonify
from .validation import BusinessValidationError, PropertyExistError
from application.security import user_datastore
# from application.access import acs_user_email
from application.cache import cache
from flask_security import hash_password
from application.db import db, User
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt 
from werkzeug.security import check_password_hash
from flask_security import verify_password

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

output_fields = {
    'email': fields.String,
    'password': fields.String,
}


class LoginAPI(Resource):
    def post(self):
        args = parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', message='Email is required')

        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', message='Password is required')

        user = db.session.query(User).filter_by(email=email).first()

        print(user, verify_password(password, user.password))
        # check passwo
        if user and verify_password(password, user.password):
            access_token = create_access_token(identity=user.email, additional_claims={'roles': [role.name for role in user.roles], 'id':user.id})
            return {'access_token': access_token}, 200
        else:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', message='Invalid email or password')
        

