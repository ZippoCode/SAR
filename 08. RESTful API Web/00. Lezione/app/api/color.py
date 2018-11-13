from flask_restful import Resource, reqparse, inputs
from app.flask_app import api

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("r", type=inputs.int_range(0, 255), required=True, location='json')
parser.add_argument("g", type=inputs.int_range(0, 255), required=True, location='json')
parser.add_argument("b", type=inputs.int_range(0, 255), required=True, location='json')


class Color(Resource):
    def get(self, name):
        return {'name': name}

    def post(self, name):
        args = parser.parse_args()
        return {'post_name': name, 'r': args.r, 'g': args.g, 'b': args.b}


api.add_resource(Color, '/api/v0.1/color/<string:name>')
