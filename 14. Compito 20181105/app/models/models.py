from google.appengine.ext import ndb


class ArtistModel(ndb.Model):
    id = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    num_search = ndb.IntegerProperty(indexed=True, default=1)
