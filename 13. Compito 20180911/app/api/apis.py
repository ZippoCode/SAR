from flask_restful import Resource
from flask import request
from itertools import product
from string import ascii_uppercase
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError, Error

from app.flask_app import api
from app.models.models import Sala, Posto, Prenotazione


class Init(Resource):
    def post(self):
        # Delete all entities
        ndb.delete_multi(Sala.query().fetch(keys_only=True))
        # Update Cinema
        sale = list()
        # Sale: 1 - 2 - 3
        posti = list()
        for i in range(1, 4):
            for c, n in product(ascii_uppercase[:15], range(1, 11)):
                posti.append(Posto(id_posto=c + "%02d" % n))
            sale.append(Sala(id_sala='sala' + str(i), time="17:30", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="20:00", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="22:30", posti=posti))
        # Sale: 4 - 5
        posti = list()
        for i in range(4, 6):
            for c, n in product(ascii_uppercase[:8], range(1, 11)):
                posti.append(Posto(id_posto=c + "%02d" % n))
            sale.append(Sala(id_sala='sala' + str(i), time="17:30", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="20:00", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="22:30", posti=posti))
        posti = list()
        for i in range(6, 7):
            for c, n in product(ascii_uppercase[:22], range(1, 15)):
                posti.append(Posto(id_posto=c + "%02d" % n))
            sale.append(Sala(id_sala='sala' + str(i), time="17:30", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="20:00", posti=posti))
            sale.append(Sala(id_sala='sala' + str(i), time="22:30", posti=posti))
        ndb.put_multi(sale)
        return {'OK': 'Eseguito'}


class Reservations(Resource):
    def get(self, room, time):
        try:
            sala = Sala.query(Sala.id_sala == room, Sala.time == time).get()
        except BadValueError:
            return {'Error 404': 'The required projection does not exist.'}, 404
        # Get posti disponibili e occupati
        posti_reserved = list()
        posti_available = list()
        for posto in sala.posti:
            if posto.disponibile:
                posti_available.append(posto.id_posto)
            else:
                posti_reserved.append(posto.id_posto)
        return {'reserved': posti_reserved, 'available': posti_available}

    def post(self, room, time):
        try:
            sala = Sala.query(Sala.id_sala == room, Sala.time == time).get()
            user = request.get_json()['user']
            posti_richiesti = request.get_json()['reserve']
        except BadValueError:
            return {'Error 404': 'The required projection does not exist.'}, 404
        except KeyError:
            return {'Error 500': 'Invalid input data'}, 500
        for posto_richiesto, posto in product(posti_richiesti, sala.posti):
            if posto_richiesto == posto.id_posto:
                if not posto.disponibile:
                    return {'Error 403': 'Posto ' + posto_richiesto + ' already occupied'}
                else:
                    posto.disponibile = False
        try:
            prenotazione = Prenotazione.query(Prenotazione.email == user,
                                              Prenotazione.sala == room,
                                              Prenotazione.orario == time).get()
            if prenotazione:
                prenotazione.posti_prenotati = posti_richiesti
            else:
                prenotazione = Prenotazione(email=user, sala=room,
                                            orario=time, posti_prenotati=posti_richiesti)
            prenotazione.put()
            sala.put()
        except Error:
            return {'Error': 'Errore sconosciuto'}, 500
        return {'Result': 'Prenotazione effettuata con successo'}, 200


class Users(Resource):
    def get(self, email):
        prenotazioni = Prenotazione.query(Prenotazione.email == email).fetch()
        lista_prenotazioni = list()
        for p in prenotazioni:
            lista_prenotazioni.append({
                'room': p.sala,
                'time': p.orario,
                'seats': p.posti_prenotati, })
        return lista_prenotazioni


api.add_resource(Init, "/api/v0.1/init/start")
api.add_resource(Reservations, '/api/v0.1/reservations/<string:room>/<string:time>')
api.add_resource(Users, '/api/v0.1/users/<string:email>')
