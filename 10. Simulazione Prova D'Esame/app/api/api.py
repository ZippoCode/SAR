from itertools import product
from flask_restful import Resource, reqparse, inputs

from app.flask_app import api
from app.models.models import Parking

parser = reqparse.RequestParser()
parser.add_argument('state', type=inputs.boolean, location=['args', 'json'])


class Init(Resource):
    def post(self):
        """
            Reinizializza tutti i posti sullo stato di disponibile

        :return:
        """
        parking_list = list()
        try:
            for piano, numero in product(range(1, 4), range(1, 11)):
                id = piano * 100 + numero
                parking = Parking(id=id, parking_id=id)
                parking.put()
                parking_list.append({'ID': id, 'State': True})
        except TypeError:
            return {'Error': 'Error INIT'}
        return {'Parking': parking_list}


class Available(Resource):

    def get(self):
        parking_list = Parking.query(Parking.state == True).fetch()
        parking_free = list()
        for parking in parking_list:
            parking_free.append(parking.parking_id)
        return {'Slots': parking_free}


class Slot(Resource):
    def get(self, slot_id):
        if slot_id not in range(101, 111) and slot_id not in range(201, 211) and slot_id not in range(301, 311):
            return {'Error': 'Invalid Input Parameters'}, 400
        parking = Parking.get_by_id(slot_id)
        if not parking:
            return {'Error': 'Parking not found'}, 404
        else:
            return {'Slot': parking.parking_id, 'State': parking.state}

    def put(self, slot_id):
        if slot_id not in range(101, 111) and slot_id not in range(201, 211) and slot_id not in range(301, 311):
            return {'Error': 'Invalid Input Parameters'}, 400
        args = parser.parse_args()
        state = args.get('state')
        parking = Parking.get_by_id(slot_id)
        if not parking:
            return {'Error': 'Parking not found'}, 404
        parking.state = state
        parking.put()
        return {'Slot': parking.parking_id, 'State': parking.state}


api.add_resource(Init, '/api/v1.0/init')
api.add_resource(Available, '/api/v1.0/availables')
api.add_resource(Slot, '/api/v1.0/slot/<int:slot_id>')
