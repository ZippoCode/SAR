from datetime import datetime

from google.appengine.ext import ndb


class ValueID(ndb.IntegerProperty):
    def _validate(self, value):
        if value not in range(101, 111) and value not in range(201, 211) and value not in range(301, 311):
            raise TypeError('Range Error.')


class Parking(ndb.Model):
    parking_id = ValueID(indexed=True, required=True)
    state = ndb.BooleanProperty(indexed=True, default=True)


class DataCreated(ndb.DateTimeProperty):
    def _from_base_type(self, value):
        data = datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
        return data


class Booking(ndb.Model):
    user_id = ndb.StringProperty(indexed=True)
    parking = ndb.IntegerProperty(indexed=True)
    code = ndb.IntegerProperty()
    date = DataCreated(indexed=True, auto_now_add=True)
