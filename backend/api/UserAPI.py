from flask_restful import Resource, reqparse, marshal_with, fields
from .validation import BusinessValidationError, PropertyExistError
from application.security import user_datastore
from application.access import acs_user_email, acs_user_id, acs_user_all
from application.cache import cache
from flask_security import hash_password
from application.db import db, User
from flask_jwt_extended import jwt_required
from application.helpers import admin_required
from flask_jwt_extended import get_jwt_identity

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

output_fields = {
    'email': fields.String,
    'password': fields.String,
}


class UserAPI(Resource):
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

        user = acs_user_email(email)

        if user:
            raise BusinessValidationError(status_code=409, error_code='USER01', message='User already exists')

        # cache.delete_memoized(acs_user_email, email)
        default_role = user_datastore.find_role('user')  # Find the 'user' role
        user_datastore.create_user(
            email=email, password=hash_password(password), roles=[default_role])
        
        db.session.commit()
        return 'user added successfully', 201
    
    @jwt_required()
    @marshal_with(output_fields)
    def put(self, id):
        current_user_email = get_jwt_identity()
        current_user = db.session.query(User).filter_by(email=current_user_email).first()

        if current_user.id != id:
            raise BusinessValidationError(status_code=403, error_code='USER03', message='You are not allowed to update this user')
        
        args = parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)

        user = db.session.query(User).filter_by(id=id).first()
        if user:
            if email:
                user.email = email
            if password:
                user.password = hash_password(password)
            db.session.commit()
            return 'user updated successfully', 200
        else:
            raise BusinessValidationError(status_code=404, error_code='USER02', message='User not found')

    
    @admin_required()
    def delete(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return 'user deleted successfully', 200
        else:
            raise BusinessValidationError(status_code=404, error_code='USER02', message='User not found')
        
    @jwt_required()
    @marshal_with(output_fields)
    def get(self, id=None):
        if id:
            user = acs_user_id(id)
            if user:
                return user, 200
            else:
                raise BusinessValidationError(status_code=404, error_code='USER02', message='User not found')
        else:
            users = acs_user_all()
            return users, 200