from flask_restful import Resource
from google.appengine.ext import ndb

from app.flask_app import api
from app.models.home_models import Floor, Room

DICT_ID = {
    '0': 'Piano seminterrato',
    '1': 'Piano terra',
    '2': 'Primo piano'
}


class StateFloor(Resource):

    def get(self, num_floor):
        if int(num_floor) < 0 or int(num_floor) > 2:
            return {'Error': 'Invalid Input'}, 401
        name_piano = DICT_ID[num_floor]
        floor = Floor.get_by_id(name_piano)
        if not floor:
            return {'Error': 'Floor not found'}, 404
        list_rooms = list()
        for room in floor.rooms:
            list_rooms.append({
                'Name': room.name,
                'State Light Bulb': room.state_light_bulb,
                'Percentage': room.percentage
            })
        return {'Floor': floor.name, 'Rooms': list_rooms}


class EditRoom(Resource):
    def put(self, name_room):
        floor_list = Floor.query(Floor.rooms.name == 'Studio').fetch()
        for floor in floor_list:
            print(floor)
        return ""


api.add_resource(StateFloor, '/api/v1.0/state_floor/<string:num_floor>')
api.add_resource(EditRoom, '/api/v1.0/edit_floor/<string:name_room>')
