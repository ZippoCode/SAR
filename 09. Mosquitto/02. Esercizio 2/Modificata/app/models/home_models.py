from google.appengine.ext import ndb


class Room(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    state_light_bulb = ndb.BooleanProperty(default=False)
    percentage = ndb.IntegerProperty()


class Floor(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    rooms = ndb.StructuredProperty(Room, repeated=True)
