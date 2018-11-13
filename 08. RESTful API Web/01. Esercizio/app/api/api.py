from flask_restful import Resource, reqparse, inputs
from app.flask_app import api
from app.models.color import Color, create_color
from google.appengine.ext import ndb

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("r", type=inputs.int_range(0, 255), required=True, location='json')
parser.add_argument("g", type=inputs.int_range(0, 255), required=True, location='json')
parser.add_argument("b", type=inputs.int_range(0, 255), required=True, location='json')


class APIColorList(Resource):

    def get(self):
        color_query = Color.query()
        colors = color_query.fetch()
        colors = [color.to_dict() for color in colors]
        return colors


class APIColor(Resource):

    def get(self, name):
        color = Color.get_by_id(name)
        if color:
            return color.to_dict()
        return 'Color not found.'

    def post(self, name):
        args = parser.parse_args()
        color = create_color(name, args.r, args.g, args.b)
        color.put()
        return color.to_dict()

    def put(self, name):
        args = parser.parse_args()
        color = Color.get_by_id(name)
        if color:
            color = create_color(name, args.r, args.g, args.b)
            color.put()
            return color.to_dict()
        else:
            return 'Color not found.'

    def delete(self, name):
        e = ndb.Key('Color', name).get()
        if e:
            e.key.delete()
            return 'Color deleted'
        return 'Color not found.'


api.add_resource(APIColorList, '/api/v0.1/color/')
api.add_resource(APIColor, '/api/v0.1/color/<string:name>')
