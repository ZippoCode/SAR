from google.appengine.ext import ndb


class Posto(ndb.Model):
    id_posto = ndb.StringProperty(indexed=True)
    disponibile = ndb.BooleanProperty(indexed=True, default=True)


sala_name = ['sala1', 'sala2', 'sala3', 'sala4', 'sala5', 'sala6']


class Sala(ndb.Model):
    id_sala = ndb.StringProperty(indexed=True, choices=sala_name)
    time = ndb.StringProperty(indexed=True, choices=["17:30", "20:00", "22:30"])
    posti = ndb.StructuredProperty(Posto, repeated=True)


class Prenotazione(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    sala = ndb.StringProperty(indexed=True)
    orario = ndb.StringProperty(indexed=True, choices=["17:30", "20:00", "22:30"])
    posti_prenotati = ndb.StringProperty(repeated=True)

