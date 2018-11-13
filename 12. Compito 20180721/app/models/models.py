from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError

choices_time = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '24:00']
choices_rule = ['night', 'sunrise', 'evenight']


class Intensity(ndb.IntegerProperty):
    def _validate(self, value):
        if value < 0 or value > 100:
            raise BadValueError('Range dei valori errato')


class CityModel(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    zone = ndb.StringProperty(indexed=True)
    rule = ndb.StringProperty(indexed=True, choices=choices_rule)
    time = ndb.StringProperty(indexed=True, choices=choices_time)
    intensity = Intensity(indexed=True)
