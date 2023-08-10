from flask_restful import Resource, reqparse, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class TestAUTHAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user, get_jwt().get('roles'))
        return {'images': ['1.avif','2.avif', '3.avif', '4.avif' ]}, 200