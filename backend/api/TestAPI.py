# create a test api that returns a basic json

from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request
class TestAPI(Resource):
    def get(self):
        query = request.args.get('query')
        return {'images': ['1.avif','2.avif', '3.avif', '4.avif', query ]}, 200