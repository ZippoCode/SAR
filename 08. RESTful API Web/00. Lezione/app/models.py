from google.appengine.ext import ndb


class Color(ndb.Model):
    label = ndb.StringProperty(required=True, indexes=True)
    red = ndb.IntegerProperty(required=True)
    green = ndb.IntegerProperty(required=True)
    blue = ndb.IntegerProperty(required=True)
