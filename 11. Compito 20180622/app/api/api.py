import base64
from flask_restful import Resource, reqparse

from app.flask_app import api
from app.models.models import Sondaggio

parser = reqparse.RequestParser()
parser.add_argument('title', type=unicode, location=['args', 'json'], help='Aggiungere la domanda', )
parser.add_argument('vote', type=bytes, location=['args', 'json'], help='Inserirre un valore')
parser.add_argument('type', type=str, choices=['P', 'N', 'A'], default='P', location=['args', 'json'],
                    help='Valori consentiti: P, N ed A.')


class Polls(Resource):
    def get(self):
        sondaggi_list = Sondaggio.query().fetch()
        sondaggi_text = list()
        for sondaggio in sondaggi_list:
            sondaggi_text.append(sondaggio.encode)
        return {'polls': sondaggi_text}, 200


class Poll(Resource):
    def post(self):
        args = parser.parse_args()
        testo = args.get('title')
        if len(testo) == 0 or testo.isdigit():
            return {'Error': 'Invalid Input.'}, 400
        sondaggio = Sondaggio.get_by_id(testo)
        if sondaggio:
            return {'Info': 'The given title already exists.'}, 409
        sondaggio = Sondaggio(
            id=testo,
            encode=testo,
            title=testo,
        )
        sondaggio.put()
        return {'id': sondaggio.encode, 'title': sondaggio.title}, 201


class PollID(Resource):
    def get(self, poll_id):
        if not poll_id:
            return {'Error': 'Invalid input parameters.'}
        sondaggio = Sondaggio.get_by_id(base64.urlsafe_b64decode(str(poll_id)))
        if not sondaggio:
            return {'Error': 'Sondaggio not found'}, 404
        dict_value = {
            'P': sondaggio.positivi,
            'N': sondaggio.negativi,
            'A': sondaggio.astenuti
        }
        return {'title': sondaggio.title, 'value': dict_value}

    def put(self, poll_id):
        args = parser.parse_args()
        value = args.get('vote')
        if value != 'P' and value != 'N' and value != 'A':
            return {'Error': 'Invalid Input Parameters'}, 400
        sondaggio = Sondaggio.get_by_id(base64.urlsafe_b64decode(str(poll_id)))
        if not sondaggio:
            return {'Error': 'Il Sondaggio non esiste'}, 404
        if value == 'P':
            sondaggio.positivi += 1
        elif value == 'N':
            sondaggio.negativi += 1
        elif value == 'A':
            sondaggio.astenuti += 1
        sondaggio.put()
        dict_value = {
            'P': sondaggio.positivi,
            'N': sondaggio.negativi,
            'A': sondaggio.astenuti
        }
        return {'Value': dict_value}, 200


class OrderPools(Resource):
    def get(self):
        """
            Ritorna la lista ordinata dei polls.

        :param poll_id:
        :return:
        """
        args = parser.parse_args()
        type = args.get('type')
        if type == 'P':
            polls_query = Sondaggio.query().order(-Sondaggio.positivi)
        elif type == 'A':
            polls_query = Sondaggio.query().order(-Sondaggio.astenuti)
        else:
            polls_query = Sondaggio.query().order(-Sondaggio.negativi)
        polls_list = list()
        for poll in polls_query.fetch():
            poll_dict = {
                'POLL ID': poll.encode,
                'POLL TITLE': poll.title,
                'POSITIVI': poll.positivi,
                'NEGATIVI': poll.negativi,
                'ASTENUTI': poll.astenuti,
            }
            polls_list.append(poll_dict)
        return {'Polls': polls_list}


api.add_resource(Polls, '/api/v0.1/polls')
api.add_resource(OrderPools, '/api/v0.1/orderpolls/')
api.add_resource(Poll, '/api/v0.1/poll')
api.add_resource(PollID, '/api/v0.1/poll/<string:poll_id>')
